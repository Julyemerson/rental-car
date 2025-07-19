CREATE TABLE IF NOT EXISTS vehicle (
  id INT AUTO_INCREMENT PRIMARY KEY,
  brand VARCHAR(255) NOT NULL, 
  model VARCHAR(255) NOT NULL, 
  vehicle_type ENUM('car', 'motorcycle') NOT NULL, 
  year INT NOT NULL, 
  license_plate VARCHAR(10) UNIQUE NOT NULL, 
  color VARCHAR(100),
  mileage INT NOT NULL DEFAULT 0, 
  available BOOLEAN NOT NULL DEFAULT TRUE,
  daily_charge DECIMAL(10,2),
  registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  ) ENGINE=InnoDB DEFAULT CHARSET=latin1

CREATE TABLE IF NOT EXISTS user (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  cpf VARCHAR(11),
  email VARCHAR(100) UNIQUE NOT NULL,
  birth_at DATE NOT NULL
  ) ENGINE=InnoDB DEFAULT CHARSET=latin1

CREATE TABLE IF NOT EXISTS employee (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  cpf VARCHAR(11),
  email VARCHAR(100) UNIQUE NOT NULL,
  role VARCHAR(100)
  ) ENGINE=InnoDB DEFAULT CHARSET=latin1

CREATE TABLE IF NOT EXISTS rental (
  id INT AUTO_INCREMENT PRIMARY KEY,
  rent_date DATE NOT NULL DEFAULT CURRENT_DATE,
  return_date DATE NOT NULL, 
  rent_value INT NOT NULL, 
  id_user INT,
  id_vehicle INT,
  id_employee INT, 
  
  FOREIGN KEY (id_user) REFERENCES user(id) ON DELETE CASCADE,
  FOREIGN KEY (id_vehicle) REFERENCES vehicle(id) ON DELETE CASCADE,
  FOREIGN KEY (id_employee) REFERENCES employee(id) ON DELETE CASCADE
  ) ENGINE=InnoDB DEFAULT CHARSET=latin1

-- Inserting sample data into the vehicle table
INSERT INTO vehicle (brand, model, vehicle_type, year, license_plate, color, mileage, available, daily_charge) 
VALUES ('Fiat', 'Strada Freedom', 'car', 2023, 'RGH1A23', 'Branco', 15000, TRUE, 120.50);

INSERT INTO vehicle (brand, model, vehicle_type, year, license_plate, color, mileage, available, daily_charge) 
VALUES ('Chevrolet', 'Onix Plus', 'car', 2024, 'SDE2B45', 'Prata', 5000, TRUE, 95.00);

INSERT INTO vehicle (brand, model, vehicle_type, year, license_plate, color, mileage, available, daily_charge) 
VALUES ('Hyundai', 'HB20 Comfort', 'car', 2022, 'JKL3C67', 'Preto', 35000, FALSE, 89.90);

INSERT INTO vehicle (brand, model, vehicle_type, year, license_plate, color, mileage, available, daily_charge) 
VALUES ('Honda', 'CG 160 Titan', 'motorcycle', 2024, 'MNO4D89', 'Vermelho', 2000, TRUE, 55.00);

INSERT INTO vehicle (brand, model, vehicle_type, year, license_plate, color, mileage, available, daily_charge) 
VALUES ('Yamaha', 'Fazer FZ25 ABS', 'motorcycle', 2023, 'PQR5E01', 'Azul', 8500, TRUE, 70.00);

-- Inserting sample data into the employee table
-- User 1
INSERT INTO user (name, last_name, cpf, email, birth_at)
VALUES ('João', 'Silva', '12345678901', 'joao.silva@example.com', '1990-05-15');

-- User 2
INSERT INTO user (name, last_name, cpf, email, birth_at)
VALUES ('Maria', 'Oliveira', '23456789012', 'maria.oliveira@example.com', '1985-11-20');

-- User 3
INSERT INTO user (name, last_name, cpf, email, birth_at)
VALUES ('Pedro', 'Santos', '34567890123', 'pedro.santos@example.com', '1998-02-10');

-- User 4
INSERT INTO user (name, last_name, cpf, email, birth_at)
VALUES ('Ana', 'Souza', '45678901234', 'ana.souza@example.com', '2001-07-30');

-- User 5
INSERT INTO user (name, last_name, cpf, email, birth_at)
VALUES ('Lucas', 'Pereira', '56789012345', 'lucas.pereira@example.com', '1995-09-05');


-- Inserting sample data into the employee table
-- Employee 1: A manager
INSERT INTO employee (name, last_name, cpf, email, role)
VALUES ('Carlos', 'Ferreira', '98765432109', 'carlos.ferreira@example.com', 'Gerente');

-- Employee 2: A rental agent
INSERT INTO employee (name, last_name, cpf, email, role)
VALUES ('Fernanda', 'Almeida', '87654321098', 'fernanda.almeida@example.com', 'Atendente');

-- Employee 3: Another rental agent
INSERT INTO employee (name, last_name, cpf, email, role)
VALUES ('Ricardo', 'Gomes', '76543210987', 'ricardo.gomes@example.com', 'Atendente');

-- Inserting sample data into the rental table
-- Rental 1: João rents a Fiat Strada, assisted by Fernanda.
INSERT INTO rental (rent_date, return_date, rent_value, id_user, id_vehicle, id_employee)
VALUES ('2025-07-18', '2025-07-23', 603, 1, 1, 2);

-- Rental 2: Maria rents a Honda CG 160 motorcycle, assisted by Ricardo.
INSERT INTO rental (rent_date, return_date, rent_value, id_user, id_vehicle, id_employee)
VALUES ('2025-07-19', '2025-07-29', 550, 2, 4, 3);

-- Rental 3: Pedro rents a Chevrolet Onix, assisted by Fernanda.
INSERT INTO rental (rent_date, return_date, rent_value, id_user, id_vehicle, id_employee)
VALUES ('2025-07-19', '2025-07-26', 665, 3, 2, 2);

-- Rental 4: Ana rents a Yamaha Fazer motorcycle, assisted by Ricardo.
INSERT INTO rental (rent_date, return_date, rent_value, id_user, id_vehicle, id_employee)
VALUES ('2025-07-17', '2025-07-20', 210, 4, 5, 3);

-- Rental 5: A past rental for Lucas with the Hyundai HB20, which is currently unavailable.
INSERT INTO rental (rent_date, return_date, rent_value, id_user, id_vehicle, id_employee)
VALUES ('2025-07-10', '2025-07-19', 809, 5, 3, 2);



