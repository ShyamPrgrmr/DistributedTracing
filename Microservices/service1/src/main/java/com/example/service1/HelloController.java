package com.example.service1;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@RestController
public class HelloController {
    private static final Logger logger = LoggerFactory.getLogger(HelloController.class);
    @Value("${SERVICE2_URL:http://service2:8080}")
    private String service2Url;

    private final RestTemplate restTemplate = new RestTemplate();

    @GetMapping("/call-service2")
    public String callService2() {
        logger.info("Calling Service2 at {}", service2Url + "/data");
        String response = restTemplate.getForObject(service2Url + "/data", String.class);
        logger.info("Received response from Service2: {}", response);
        return "Service1 got: " + response;
    }
}
