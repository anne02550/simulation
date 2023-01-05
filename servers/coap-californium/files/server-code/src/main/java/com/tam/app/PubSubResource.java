package com.tam.app;

import org.eclipse.californium.core.CoapResource;
import org.eclipse.californium.core.server.resources.CoapExchange;
import org.eclipse.californium.core.coap.CoAP.ResponseCode;

public class PubSubResource extends CoapResource {

    private volatile String resource = "";

    public PubSubResource() {
        super("some-resource");
        setObservable(true);
        getAttributes().setTitle("pub-sub Resource");
    }

    @Override
    public void handlePOST(CoapExchange exchange) {
        System.out.println("POST ON PubSubResource CALLED");
        resource = exchange.getRequestText();
        System.out.println(resource);
        exchange.respond(ResponseCode.CHANGED);
        changed();
    }
}