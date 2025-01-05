package com.example.zoo_kafka_app_b;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class ZooKafkaAppBApplication {
	public static void main(String[] args) {
		SpringApplication.run(ZooKafkaAppBApplication.class, args);
	}
}
