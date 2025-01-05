package com.example.task_service;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

/**
 * Repository interface for Task entities.
 */
@Repository
public interface TaskRepository extends JpaRepository<Task, Long> {
    List<Task> findByTitle(String title);

    List<Task> findByDescription(String description);

    List<Task> findByStatus(String status);

    List<Task> findByCreatedAt(LocalDateTime createdAt);
}
