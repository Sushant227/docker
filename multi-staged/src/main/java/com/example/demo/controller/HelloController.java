package com.example.demo.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {

    @GetMapping("/")
    public String hello() {
        return "Hello from the Dockerized Spring Boot app!";
    }

    @GetMapping("/health")
    public String health() {
        return "OK";
    }

}
