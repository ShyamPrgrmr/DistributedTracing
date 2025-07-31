package com.example.service2;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.beans.factory.annotation.Autowired;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@RestController
public class DataController {
    private static final Logger logger = LoggerFactory.getLogger(DataController.class);

    @Autowired
    private MessageRepository messageRepository;

    @GetMapping("/data")
    public String getData() {
        logger.info("Fetching all messages from the database");
        List<Message> messages = messageRepository.findAll();
        if (messages.isEmpty()) {
            logger.warn("No messages found in the database");
            return "No messages in DB.";
        }
        String result = messages.stream().map(Message::getText).reduce((a, b) -> a + ", " + b).orElse("");
        logger.info("Returning messages: {}", result);
        return "DB Messages: " + result;
    }
}
