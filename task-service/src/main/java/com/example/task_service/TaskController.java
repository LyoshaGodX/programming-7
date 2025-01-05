package com.example.task_service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;

/**
 * REST controller for managing tasks.
 */
@RestController
@RequestMapping("/api/tasks")
public class TaskController {

    @Autowired
    private TaskRepository taskRepository;

    /**
     * Get all tasks.
     *
     * @return a list of all tasks
     */
    @GetMapping
    public List<Task> getAllTasks() {
        return taskRepository.findAll();
    }

    /**
     * Create a new task.
     *
     * @param task the task to create
     * @return the created task
     */
    @PostMapping
    public Task createTask(@RequestBody Task task) {
        task.setCreatedAt(LocalDateTime.now());
        return taskRepository.save(task);
    }

    /**
     * Update an existing task.
     *
     * @param id          the id of the task to update
     * @param updatedTask the updated task details
     * @return the updated task
     */
    @PutMapping("/{id}")
    public Task updateTask(@PathVariable Long id, @RequestBody Task updatedTask) {
        return taskRepository.findById(id)
                .map(task -> {
                    task.setTitle(updatedTask.getTitle());
                    task.setDescription(updatedTask.getDescription());
                    task.setStatus(updatedTask.getStatus());
                    return taskRepository.save(task);
                })
                .orElseThrow(() -> new RuntimeException("Task not found with id " + id));
    }

    /**
     * Delete a task.
     *
     * @param id the id of the task to delete
     */
    @DeleteMapping("/{id}")
    public void deleteTask(@PathVariable Long id) {
        taskRepository.deleteById(id);
    }

    /**
     * Find tasks by title.
     *
     * @param title the title of the tasks to find
     * @return a list of tasks with the specified title
     */
    @GetMapping("/title/{title}")
    public List<Task> getTasksByTitle(@PathVariable String title) {
        return taskRepository.findByTitle(title);
    }

    /**
     * Find tasks by description.
     *
     * @param description the description of the tasks to find
     * @return a list of tasks with the specified description
     */
    @GetMapping("/description/{description}")
    public List<Task> getTasksByDescription(@PathVariable String description) {
        return taskRepository.findByDescription(description);
    }

    /**
     * Find tasks by status.
     *
     * @param status the status of the tasks to find
     * @return a list of tasks with the specified status
     */
    @GetMapping("/status/{status}")
    public List<Task> getTasksByStatus(@PathVariable String status) {
        return taskRepository.findByStatus(status);
    }

    /**
     * Find tasks by creation timestamp.
     *
     * @param createdAt the creation timestamp of the tasks to find
     * @return a list of tasks with the specified creation timestamp
     */
    @GetMapping("/createdAt/{createdAt}")
    public List<Task> getTasksByCreatedAt(@PathVariable LocalDateTime createdAt) {
        return taskRepository.findByCreatedAt(createdAt);
    }
}
