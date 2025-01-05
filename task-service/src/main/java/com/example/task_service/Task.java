package com.example.task_service;

import jakarta.persistence.*;
import java.time.LocalDateTime;

/**
 * Represents a task with a title, description, status, and creation timestamp.
 */
@Entity
public class Task {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String title;
    private String description;
    private String status; // For example, "Pending", "In Progress", "Completed"
    private LocalDateTime createdAt;

    /**
     * Default constructor.
     */
    public Task() {
    }

    /**
     * Constructs a new Task with the specified title, description, status, and
     * creation timestamp.
     *
     * @param title       the title of the task
     * @param description the description of the task
     * @param status      the status of the task
     * @param createdAt   the creation timestamp of the task
     */
    public Task(String title, String description, String status, LocalDateTime createdAt) {
        this.title = title;
        this.description = description;
        this.status = status;
        this.createdAt = createdAt;
    }

    // Getters and setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
