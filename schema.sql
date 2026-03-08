-- ============================================================
--  Narayanan's Catering Workforce Management System
--  MySQL Schema — for local development
-- ============================================================

CREATE DATABASE IF NOT EXISTS catering_wms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE catering_wms;

-- ─── USERS ────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    username   VARCHAR(100) UNIQUE NOT NULL,
    password   VARCHAR(256) NOT NULL,
    role       ENUM('manager','worker') NOT NULL,
    phone      VARCHAR(20),
    created_at DATETIME DEFAULT NOW()
);

-- ─── WORKERS ──────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS workers (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    user_id           INT,
    name              VARCHAR(150) NOT NULL,
    phone             VARCHAR(20) UNIQUE NOT NULL,
    skill             ENUM('Cook','Server','Helper','Supervisor') NOT NULL,
    experience_years  INT DEFAULT 0,
    daily_wage        DECIMAL(10,2) DEFAULT 500.00,
    is_available      TINYINT(1) DEFAULT 1,
    address           TEXT,
    emergency_contact VARCHAR(150),
    created_at        DATETIME DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- ─── EVENTS ───────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS events (
    id                   INT AUTO_INCREMENT PRIMARY KEY,
    event_name           VARCHAR(200) NOT NULL,
    client_name          VARCHAR(150) NOT NULL,
    event_date           DATE NOT NULL,
    event_time           VARCHAR(10) DEFAULT '09:00',
    location             TEXT NOT NULL,
    event_type           VARCHAR(80) DEFAULT 'Lunch',
    required_cooks       INT DEFAULT 0,
    required_servers     INT DEFAULT 0,
    required_helpers     INT DEFAULT 0,
    required_supervisors INT DEFAULT 0,
    status               ENUM('upcoming','ongoing','completed','cancelled') DEFAULT 'upcoming',
    notes                TEXT,
    created_by           INT,
    created_at           DATETIME DEFAULT NOW(),
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

-- ─── EVENT ASSIGNMENTS ────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS event_assignments (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    event_id    INT NOT NULL,
    worker_id   INT NOT NULL,
    assigned_by INT,
    status      ENUM('assigned','confirmed','rejected','attended','absent') DEFAULT 'assigned',
    assigned_at DATETIME DEFAULT NOW(),
    UNIQUE KEY uq_event_worker (event_id, worker_id),
    FOREIGN KEY (event_id)    REFERENCES events(id)  ON DELETE CASCADE,
    FOREIGN KEY (worker_id)   REFERENCES workers(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_by) REFERENCES users(id)   ON DELETE SET NULL
);

-- ─── LEAVE REQUESTS ───────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS leave_requests (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    worker_id        INT NOT NULL,
    event_id         INT NOT NULL,
    reason           TEXT NOT NULL,
    status           ENUM('pending','approved','rejected') DEFAULT 'pending',
    manager_response TEXT,
    requested_at     DATETIME DEFAULT NOW(),
    responded_at     DATETIME,
    FOREIGN KEY (worker_id) REFERENCES workers(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id)  REFERENCES events(id)  ON DELETE CASCADE
);

-- ─── ATTENDANCE ───────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS attendance (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    event_id       INT NOT NULL,
    worker_id      INT NOT NULL,
    status         ENUM('present','absent','late') NOT NULL,
    check_in_time  VARCHAR(10),
    recorded_by    INT,
    recorded_at    DATETIME DEFAULT NOW(),
    UNIQUE KEY uq_att (event_id, worker_id),
    FOREIGN KEY (event_id)   REFERENCES events(id)  ON DELETE CASCADE,
    FOREIGN KEY (worker_id)  REFERENCES workers(id) ON DELETE CASCADE,
    FOREIGN KEY (recorded_by) REFERENCES users(id)  ON DELETE SET NULL
);

-- ─── PAYMENTS ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS payments (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    worker_id      INT NOT NULL,
    event_id       INT,
    amount         DECIMAL(10,2) NOT NULL,
    payment_method ENUM('UPI','Credit Card','Cash','Bank Transfer') DEFAULT 'UPI',
    payment_status ENUM('pending','paid','failed') DEFAULT 'pending',
    transaction_id VARCHAR(100),
    paid_at        DATETIME,
    notes          TEXT,
    created_at     DATETIME DEFAULT NOW(),
    FOREIGN KEY (worker_id) REFERENCES workers(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id)  REFERENCES events(id)  ON DELETE SET NULL
);

-- ─── NOTIFICATIONS ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS notifications (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    user_id    INT NOT NULL,
    message    TEXT NOT NULL,
    is_read    TINYINT(1) DEFAULT 0,
    created_at DATETIME DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ─── DEFAULT ADMIN ────────────────────────────────────────────────────────────
-- Default manager: admin / admin123
-- SHA-256 of "admin123" = 240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9
INSERT IGNORE INTO users (username, password, role, phone)
VALUES ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'manager', '9080599509');
