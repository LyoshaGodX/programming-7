package com.example.zoo_kafka_app_b;

import java.util.UUID;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class KafkaProducerB {
    private static final Logger logger = LoggerFactory.getLogger(KafkaProducerB.class);

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    @Scheduled(fixedRate = 5000)
    public void sendMessage() {
        try {
            String message = "Message from AppB: " + UUID.randomUUID();
            kafkaTemplate.send("appB-to-appA", message);
            logger.info("AppB sent: {}", message);
        } catch (Exception e) {
            logger.error("Failed to send message: {}", e.getMessage(), e);
        }
    }
}