package com.tam.app;

import com.tam.app.PubSubResource;

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
import org.eclipse.californium.elements.config.UdpConfig;

public class App extends CoapServer {

	public static int PORT = 5683;

	static {
		CoapConfig.register();
		UdpConfig.register();
	}

	public static void main(String[] args) {
		try {

			App server = new App();

			System.out.println("\nstarting server");
			server.start();

		} catch (SocketException | java.net.UnknownHostException e) {
			System.err.println("Failed to initialize server: " + e.getMessage());
		}
	}

	public App() throws SocketException, java.net.UnknownHostException {
		add(new PubSubResource());

        Configuration config = Configuration.getStandard();

        System.out.printf("Adding udp listener to %s", PORT);

        InetSocketAddress bindToAddress = new InetSocketAddress(PORT);
        CoapEndpoint.Builder builder = new CoapEndpoint.Builder();
        builder.setInetSocketAddress(bindToAddress);
        builder.setConfiguration(config);
        addEndpoint(builder.build());
	}
}
