package com.example.zoo_kafka_app_a;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class KafkaConsumerA {
    private static final Logger logger = LoggerFactory.getLogger(KafkaConsumerA.class);

    @KafkaListener(topics = "appB-to-appA", groupId = "appAGroup")
    public void consumeMessage(String message) {
        logger.info("AppA received: {}", message);
    }
}