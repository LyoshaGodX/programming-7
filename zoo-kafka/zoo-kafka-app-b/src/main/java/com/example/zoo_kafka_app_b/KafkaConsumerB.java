package com.example.zoo_kafka_app_b;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class KafkaConsumerB {
    private static final Logger logger = LoggerFactory.getLogger(KafkaConsumerB.class);

    @KafkaListener(topics = "appA-to-appB", groupId = "appBGroup")
    public void consumeMessage(String message) {
        logger.info("AppB received: {}", message);
    }
}