package com.example.zoo_kafka_app_a;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class ZooKafkaAppAApplication {
    public static void main(String[] args) {
        SpringApplication.run(ZooKafkaAppAApplication.class, args);
    }
}
