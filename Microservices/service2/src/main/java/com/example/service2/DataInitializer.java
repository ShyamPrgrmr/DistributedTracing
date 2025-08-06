package com.example.service2;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import org.springframework.beans.factory.annotation.Autowired;

@Component
public class DataInitializer implements CommandLineRunner {

    @Autowired
    private MessageRepository messageRepository;

    @Override
    public void run(String... args) throws Exception {
        if (messageRepository.count() == 0) {
            messageRepository.save(new Message("Hello from DB!"));
            messageRepository.save(new Message("Another message"));
        }
    }
}
