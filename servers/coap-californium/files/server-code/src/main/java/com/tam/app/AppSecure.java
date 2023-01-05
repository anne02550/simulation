package com.tam.app;

import com.tam.app.PubSubResource;

import java.io.File;
import java.util.List;
import java.util.Arrays;
import java.util.ArrayList;

import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.SocketException;

import org.eclipse.californium.core.CoapResource;
import org.eclipse.californium.core.CoapServer;
import org.eclipse.californium.core.coap.CoAP.ResponseCode;
import org.eclipse.californium.core.config.CoapConfig;
import org.eclipse.californium.core.network.CoapEndpoint;
import org.eclipse.californium.core.server.resources.CoapExchange;
import org.eclipse.californium.elements.config.Configuration;
import org.eclipse.californium.scandium.config.DtlsConfig;

import org.eclipse.californium.elements.config.Configuration.DefinitionsProvider;
import org.eclipse.californium.scandium.config.DtlsConfig.DtlsRole;
import org.eclipse.californium.scandium.dtls.cipher.CipherSuite;

import org.eclipse.californium.scandium.DTLSConnector;
import org.eclipse.californium.scandium.MdcConnectionListener;
import org.eclipse.californium.scandium.config.DtlsConnectorConfig;

import javax.net.ssl.KeyManager;
import javax.net.ssl.X509KeyManager;

import org.eclipse.californium.elements.util.SslContextUtil;
import org.eclipse.californium.scandium.dtls.CertificateType;
import org.eclipse.californium.scandium.dtls.cipher.CipherSuite.KeyExchangeAlgorithm;
import org.eclipse.californium.scandium.dtls.x509.KeyManagerCertificateProvider;
import org.eclipse.californium.scandium.dtls.x509.StaticNewAdvancedCertificateVerifier;
import org.eclipse.californium.scandium.dtls.x509.StaticNewAdvancedCertificateVerifier.Builder;

import java.io.IOException;
import java.security.GeneralSecurityException;
import java.security.cert.Certificate;

public class AppSecure extends CoapServer {

    public enum Mode {
		/**
		 * Preshared secret keys.
		 */
		PSK,
		/**
		 * EC DHE, preshared secret keys.
		 */
		ECDHE_PSK,
		/**
		 * Raw public key certificates.
		 */
		RPK,
		/**
		 * X.509 certificates.
		 */
		X509,
		/**
		 * raw public key certificates just trusted (client only).
		 */
		RPK_TRUST,
		/**
		 * X.509 certificates just trusted (client only).
		 */
		X509_TRUST,
		/**
		 * Client authentication wanted (server only).
		 */
		WANT_AUTH,
		/**
		 * No client authentication (server only).
		 */
		NO_AUTH,
	}

    public static int PORT = 5684;

    static {
		CoapConfig.register();
		DtlsConfig.register();
	}

    public static void main(String[] args) {
		try {
			AppSecure server = new AppSecure();
			System.out.println("starting server");
			server.start();
		} catch (SocketException | java.net.UnknownHostException e) {
			System.err.println("Failed to initialize server: " + e.getMessage());
		}
	}

	public AppSecure() throws SocketException, java.net.UnknownHostException {
		add(new PubSubResource());

        InetAddress addr = InetAddress.getByName("192.168.1.220");

        File CONFIG_FILE = new File("Californium3SecureServer.properties");
        String CONFIG_HEADER = "Californium CoAP Properties file for Secure Server";
        DefinitionsProvider definitionsProvider = new DefinitionsProvider() {
            @Override
            public void applyDefinitions(Configuration config) {
                config.set(DtlsConfig.DTLS_ROLE, DtlsRole.SERVER_ONLY);
                config.set(DtlsConfig.DTLS_RECOMMENDED_CIPHER_SUITES_ONLY, false);
                config.set(DtlsConfig.DTLS_PRESELECTED_CIPHER_SUITES, CipherSuite.STRONG_ENCRYPTION_PREFERENCE);
            }
        };

        Configuration config = Configuration.createWithFile(CONFIG_FILE, CONFIG_HEADER, definitionsProvider);

        DtlsConnectorConfig.Builder builder = DtlsConnectorConfig.builder(config)
				.setAddress(new InetSocketAddress(PORT));

        String certificateAlias = "server.*";
		Configuration configuration = builder.getIncompleteConfig().getConfiguration();
		Builder trustBuilder = StaticNewAdvancedCertificateVerifier.builder();
        try {
            // try to read certificates
            KeyManager[] credentials = SslContextUtil.loadKeyManager(SslContextUtil.CLASSPATH_SCHEME + "certs/keyStore.jks", certificateAlias, "endPass".toCharArray(), "endPass".toCharArray());

            Certificate[] trustedCertificates = SslContextUtil.loadTrustedCertificates(
                    SslContextUtil.CLASSPATH_SCHEME + "certs/trustStore.jks", "root", "rootPass".toCharArray());
            trustBuilder.setTrustedCertificates(trustedCertificates);
            trustBuilder.setTrustAllRPKs();

            List<CertificateType> types = new ArrayList<>();
            types.add(CertificateType.RAW_PUBLIC_KEY);
            types.add(CertificateType.X_509);

            X509KeyManager keyManager = SslContextUtil.getX509KeyManager(credentials);
            KeyManagerCertificateProvider certificateProvider = new KeyManagerCertificateProvider(keyManager, types);
            builder.setCertificateIdentityProvider(certificateProvider);

        } catch (GeneralSecurityException e) {
            e.printStackTrace();
            throw new IllegalArgumentException(e.getMessage());
        } catch (IOException e) {
            e.printStackTrace();
            System.err.println("certificates are missing!");
            throw new IllegalArgumentException(e.getMessage());
        }

		if (trustBuilder.hasTrusts()) {
			builder.setAdvancedCertificateVerifier(trustBuilder.build());
		}

		List<CipherSuite> ciphers = configuration.get(DtlsConfig.DTLS_PRESELECTED_CIPHER_SUITES);
		List<CipherSuite> selectedCiphers = new ArrayList<>();
		for (CipherSuite cipherSuite : ciphers) {
			KeyExchangeAlgorithm keyExchange = cipherSuite.getKeyExchange();
			if (keyExchange == KeyExchangeAlgorithm.PSK || keyExchange == KeyExchangeAlgorithm.ECDHE_PSK || keyExchange == KeyExchangeAlgorithm.EC_DIFFIE_HELLMAN) {
                selectedCiphers.add(cipherSuite);
			}
		}
		configuration.set(DtlsConfig.DTLS_PRESELECTED_CIPHER_SUITES, selectedCiphers);
		builder.setConnectionListener(new MdcConnectionListener());

		DTLSConnector connector = new DTLSConnector(builder.build());
		CoapEndpoint.Builder coapBuilder = new CoapEndpoint.Builder()
				.setConfiguration(config)
				.setConnector(connector);

        addEndpoint(coapBuilder.build());

		// add special interceptor for message traces
		System.out.println("Secure CoAP server powered by Scandium (Sc) is listening on port " + PORT);
	}
}
