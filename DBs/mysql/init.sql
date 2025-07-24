CREATE TABLE application_partition_mapping (
    id INT AUTO_INCREMENT PRIMARY KEY,
    application_id INT NOT NULL,
    partition_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_app_partition (application_id, partition_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
