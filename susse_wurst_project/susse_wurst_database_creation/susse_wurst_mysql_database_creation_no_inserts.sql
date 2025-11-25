/*****************************************************************************************
SÜSSE WURST TABLE CREATION FOR MYSQL

DEVELOPER: N.F. Desmond
DATE: November 2025
DESCRIPTION: This script implmenents MySQL database tables for the Süsse Wurst
grocery store project. The overall system consists of two connected database schemas:
  1. sw_hr - Human Resources database
  2. sw_store - Store Inventory and Supply database
A user 'hr_associate' is also created at the end of the  script to be used for logging 
into the HR GUI application.
*****************************************************************************************/

/*********** I. DROP EXISTING DATABASES ***********/

DROP DATABASE IF EXISTS sw_hr;
DROP DATABASE IF EXISTS sw_store;


/*********** II. CREATE HR AND STORE DATABASES ***********/

CREATE DATABASE sw_hr
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

CREATE DATABASE sw_store
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_as_ci;
-- the collation for sw_store is accent-sensitive to account for the 
-- various diacritical marks used in product and manufacturer names


/*********** III. CREATE HR TABLES ***********/

USE sw_hr;

CREATE TABLE store_region(
  region_id          TINYINT     UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  region_name        VARCHAR(25)          NOT NULL,
  region_description VARCHAR(100)         NOT NULL
)
ENGINE=InnoDB
COMMENT 'Tracks the regional grouping of Süsse Wurst locations';


CREATE TABLE location(
  loc_id         SMALLINT        UNSIGNED     NOT NULL PRIMARY KEY,
  loc_name       VARCHAR(50)                  NOT NULL,
  loc_address    VARCHAR(50)                  NOT NULL,
  loc_city       VARCHAR(25)                  NOT NULL,
  loc_state      CHAR(2)         DEFAULT 'AZ' NOT NULL,
  loc_zip        CHAR(5)                      NOT NULL,
  loc_phone      CHAR(12)                     NOT NULL,
  loc_start_date DATE                         NOT NULL,
  region_id      TINYINT         UNSIGNED     NOT NULL,
 CONSTRAINT loc_regid_fk FOREIGN KEY (region_id) REFERENCES store_region (region_id),
 CONSTRAINT loc_state_ck CHECK (loc_state IN ('AZ', 'NV'))
)
ENGINE=InnoDB
COMMENT 'Tracks corporate and store locations.';


CREATE TABLE employee_type(
  emp_type_id   TINYINT     UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  emp_type_name VARCHAR(25)          NOT NULL,
  emp_comp_type VARCHAR(25)          NOT NULL
)
ENGINE=InnoDB
COMMENT 'A simple table to track employment variety.';


CREATE TABLE job_position(
  position_id    TINYINT      UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  position_title VARCHAR(50)           NOT NULL,
  emp_type_id    TINYINT      UNSIGNED NOT NULL,
  min_comp       DECIMAL(8,2) UNSIGNED NOT NULL,
  max_comp       DECIMAL(8,2) UNSIGNED NOT NULL,
  head_id        TINYINT      UNSIGNED NULL,
 CONSTRAINT position_emptypeid_fk FOREIGN KEY (emp_type_id) REFERENCES employee_type (emp_type_id)
)
ENGINE=InnoDB
COMMENT 'Tracks historical and current job positions at Süsse Wurst.';


CREATE TABLE department(
  dept_id     SMALLINT    UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  dept_name   VARCHAR(50)          NOT NULL,
  loc_id      SMALLINT    UNSIGNED NOT NULL,
  head_id     TINYINT	  UNSIGNED NOT NULL,
 CONSTRAINT dept_locid_fk  FOREIGN KEY (loc_id)  REFERENCES location (loc_id)          ON DELETE CASCADE,
 CONSTRAINT dept_headid_fk FOREIGN KEY (head_id) REFERENCES job_position (position_id)
)
ENGINE=InnoDB
COMMENT 'Tracks corporate and store-level departments.';


CREATE TABLE employee(
  emp_id        MEDIUMINT  UNSIGNED NOT NULL PRIMARY KEY,
  emp_fname     VARCHAR(75)         NOT NULL,
  emp_lname     VARCHAR(75)         NOT NULL,
  emp_hire_date DATE                NOT NULL,
  emp_dob       DATE                NOT NULL,
  emp_ssn       CHAR(11)            NOT NULL,
  emp_address   VARCHAR(75)         NOT NULL, 
  emp_city      VARCHAR(75)         NOT NULL,
  emp_state     CHAR(2)             NOT NULL,
  emp_zip       CHAR(5)             NOT NULL,
  emp_phone     CHAR(12)            NOT NULL,
 CONSTRAINT emp_ssn_uq UNIQUE (emp_ssn)
)
ENGINE=InnoDB
COMMENT 'Tracks PII for past and present employees.';


CREATE TABLE active_employee(
  emp_id           MEDIUMINT    UNSIGNED NOT NULL PRIMARY KEY,
  position_id      TINYINT      UNSIGNED NOT NULL,
  dept_id          SMALLINT     UNSIGNED NOT NULL,
  active_emp_comp  DECIMAL(8,2) UNSIGNED NOT NULL,
  active_emp_email VARCHAR(100)          NOT NULL,
 CONSTRAINT activeemp_empid_fk      FOREIGN KEY (emp_id)      REFERENCES employee (emp_id)           ON UPDATE CASCADE,
 CONSTRAINT activeemp_positionid_fk FOREIGN KEY (position_id) REFERENCES job_position (position_id),
 CONSTRAINT activeemp_deptid_fk     FOREIGN KEY (dept_id)     REFERENCES department (dept_id)        ON DELETE CASCADE,
 CONSTRAINT activeemp_email_uq	    UNIQUE (active_emp_email)
)
ENGINE=InnoDB
COMMENT 'Tracks additional data for current employees.';


CREATE TABLE termination_type(
  term_type_code TINYINT     UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  term_type_name VARCHAR(25)          NOT NULL
)
ENGINE=InnoDB
COMMENT 'Tracks reasons for employee termination.';


CREATE TABLE past_employee(
  emp_id           MEDIUMINT UNSIGNED NOT NULL PRIMARY KEY,
  position_id      TINYINT   UNSIGNED NOT NULL,
  dept_id          SMALLINT  UNSIGNED NOT NULL,
  emp_term_date    DATE               NOT NULL,
  term_type_code   TINYINT   UNSIGNED NOT NULL,
 CONSTRAINT pastemp_empid_fk      FOREIGN KEY (emp_id)      REFERENCES employee (emp_id),
 CONSTRAINT pastemp_positionid_fk FOREIGN KEY (position_id) REFERENCES job_position (position_id),
 CONSTRAINT pastemp_deptid_fk     FOREIGN KEY (dept_id)     REFERENCES department (dept_id)
)
ENGINE=InnoDB
COMMENT 'Tracks historical data for former Süsse Wurst employees.';


CREATE TABLE employee_history(
  emp_hist_id MEDIUMINT UNSIGNED      NOT NULL AUTO_INCREMENT PRIMARY KEY,
  emp_id      MEDIUMINT UNSIGNED      NOT NULL,
  position_id TINYINT   UNSIGNED      NOT NULL,
  dept_id     SMALLINT  UNSIGNED      NOT NULL,
  start_date  DATE                    NOT NULL,
  end_date    DATE      DEFAULT NULL,
 CONSTRAINT emphist_empid_fk      FOREIGN KEY (emp_id)      REFERENCES active_employee (emp_id),
 CONSTRAINT emphist_positionid_fk FOREIGN KEY (position_id) REFERENCES job_position (position_id),
 CONSTRAINT emphist_deptid_fk     FOREIGN KEY (dept_id)     REFERENCES department (dept_id)
)
ENGINE=InnoDB
COMMENT 'Tracks changes in employee data such as position, location, department, and pay.';


CREATE TABLE position_opening(
  opening_id  MEDIUMINT UNSIGNED      NOT NULL AUTO_INCREMENT PRIMARY KEY,
  position_id TINYINT   UNSIGNED      NOT NULL,
  dept_id     SMALLINT  UNSIGNED      NOT NULL,
  open_date   DATE                    NOT NULL,
  close_date  DATE      DEFAULT NULL,
 CONSTRAINT opening_positionid_fk FOREIGN KEY (position_id) REFERENCES job_position (position_id),
 CONSTRAINT opening_deptid_fk     FOREIGN KEY (dept_id)     REFERENCES department (dept_id)
)
ENGINE=InnoDB
COMMENT 'Tracks position openings at Süsse Wurst.';


CREATE TABLE applicant_status(
  applicant_status_code        TINYINT     UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  applicant_status_description VARCHAR(25)          NOT NULL
)
ENGINE=InnoDB
COMMENT 'Tracks the outcome of each job applicant.';


CREATE TABLE applicant(
  applicant_id      MEDIUMINT   UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  applicant_fname   VARCHAR(75)          NOT NULL,
  applicant_lname   VARCHAR(75)          NOT NULL,
  application_date  DATE                 NOT NULL,
  applicant_dob     DATE                 NOT NULL,
  applicant_ssn     CHAR(11)             NOT NULL,
  applicant_address VARCHAR(100)         NOT NULL,
  applicant_city    VARCHAR(75)          NOT NULL,
  applicant_state   CHAR(2)              NOT NULL,
  applicant_zip     CHAR(5)              NOT NULL,
  applicant_phone   CHAR(12)             NOT NULL,
  applicant_email   VARCHAR(100)         NOT NULL,
 CONSTRAINT app_ssn_uq       UNIQUE (applicant_ssn),
 CONSTRAINT app_email_uq     UNIQUE (applicant_email)
)
ENGINE=InnoDB
COMMENT 'Tracks applicants applying for a position at Süsse Wurst.';


CREATE TABLE applicant_history(
  applicant_id          MEDIUMINT UNSIGNED NOT NULL,
  opening_id            MEDIUMINT UNSIGNED NOT NULL,
  applicant_status_code TINYINT   UNSIGNED NOT NULL,
 PRIMARY KEY (applicant_id, opening_id),
 CONSTRAINT apphist_appid_fk      FOREIGN KEY (applicant_id)	      REFERENCES applicant (applicant_id),
 CONSTRAINT apphist_openingid_fk  FOREIGN KEY (opening_id)	      REFERENCES position_opening (opening_id),
 CONSTRAINT apphist_statuscode_fk FOREIGN KEY (applicant_status_code) REFERENCES applicant_status (applicant_status_code)
)
ENGINE=InnoDB
COMMENT 'Stores historical data on applicants.';


CREATE TABLE prospective_status(
  prospective_status_code TINYINT     UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  prospective_status      VARCHAR(25)          NOT NULL
)
ENGINE=InnoDB
COMMENT 'A simple table to track status options of prospective hires.';


CREATE TABLE prospective_hire(
  prospective_id          SMALLINT  UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  applicant_id            MEDIUMINT UNSIGNED NOT NULL,
  opening_id              MEDIUMINT UNSIGNED NOT NULL,
  prospective_status_code TINYINT   UNSIGNED NOT NULL,
  change_date             DATETIME           NOT NULL,
 CONSTRAINT prosphire_appid_fk      FOREIGN KEY (applicant_id)            REFERENCES applicant (applicant_id),
 CONSTRAINT prosphire_openingid_fk  FOREIGN KEY (opening_id)              REFERENCES position_opening (opening_id),
 CONSTRAINT prosphire_statuscode_fk FOREIGN KEY (prospective_status_code) REFERENCES prospective_status (prospective_status_code)
)
ENGINE=InnoDB
COMMENT 'Tracks the current status of active applicants.';


-- modifying JOB_POSITION to make head_id a FK to position_id
ALTER TABLE job_position
  ADD CONSTRAINT position_headid_fk FOREIGN KEY (head_id) REFERENCES job_position (position_id);

                              
/*********** IV. CREATE STORE TABLES ***********/

USE sw_store;


CREATE TABLE country(
country_id               TINYINT     UNSIGNED   NOT NULL AUTO_INCREMENT PRIMARY KEY,
official_country_name    VARCHAR(100)           NOT NULL,
translated_official_name VARCHAR(100)           NOT NULL,
common_country_name      VARCHAR(100)           NOT NULL,
country_capital          VARCHAR(50)            NOT NULL
)
ENGINE=InnoDB
COMMENT 'Tracks the countries products are manufactured in and imported from.';


CREATE TABLE manufacturer(
  manu_id             SMALLINT     UNSIGNED   NOT NULL AUTO_INCREMENT PRIMARY KEY,
  manu_name           VARCHAR(100)            NOT NULL,
  country_id          TINYINT      UNSIGNED   NOT NULL,
  manu_address        VARCHAR(100)            NOT NULL,
  manu_city           VARCHAR(100)            NOT NULL,
  manu_postal_code    VARCHAR(10)             NOT NULL,
  manu_state_province VARCHAR(50)             NOT NULL,
 CONSTRAINT manu_countryid_fk FOREIGN KEY (country_id) REFERENCES country (country_id)
)
ENGINE=InnoDB
COMMENT 'Tracks product manufacturers.';


CREATE TABLE package_type(
  package_type_id   TINYINT    UNSIGNED   NOT NULL AUTO_INCREMENT PRIMARY KEY,
  package_type_name VARCHAR(50)           NOT NULL
)
ENGINE=InnoDB
COMMENT 'Tracks the various package types products come in.';


CREATE TABLE package_material(
  material_id   TINYINT     UNSIGNED  NOT NULL AUTO_INCREMENT PRIMARY KEY,
  material_name VARCHAR(50)           NOT NULL
)
ENGINE=InnoDB
COMMENT 'Tracks the various types of packaging material.';


CREATE TABLE product_type_category(
  type_category_id   TINYINT     UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  type_category_name VARCHAR(50)          NOT NULL
)
ENGINE=InnoDB
COMMENT 'Tracks broad categories for describing product types.';


CREATE TABLE product_type(
  product_type_id          SMALLINT    UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  product_type_name        VARCHAR(50)          NOT NULL,
  product_type_description VARCHAR(100)         NOT NULL,
  type_category_id         TINYINT     UNSIGNED NOT NULL,
 CONSTRAINT prodtype_catid_fk FOREIGN KEY (type_category_id) REFERENCES product_type_category (type_category_id)
)
ENGINE=InnoDB
COMMENT 'Tracks the type of each product.';


CREATE TABLE project(
  project_id                MEDIUMINT    UNSIGNED     NOT NULL AUTO_INCREMENT PRIMARY KEY,
  project_code_name         VARCHAR(50)               NOT NULL,
  project_description       VARCHAR(100)              NOT NULL,
  product_type_id           SMALLINT     UNSIGNED     NOT NULL,
  sku			                  CHAR(9)      DEFAULT      NULL,
  project_start_date        DATE                      NOT NULL,
  project_expected_end_date DATE                      NOT NULL,
  project_actual_end_date   DATE         DEFAULT      NULL,
 CONSTRAINT project_prodtypeid_fk FOREIGN KEY (product_type_id) REFERENCES product_type (product_type_id)
)
ENGINE=InnoDB
COMMENT "Tracks development projects for the Amelia's Own line.";


CREATE TABLE trial_status(
  status_id          TINYINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  status_name        VARCHAR(25)      NOT NULL,
  status_description VARCHAR(100)     NOT NULL
)
ENGINE=InnoDB
COMMENT 'Tracks the start-to-finish stages of a project trial.';


CREATE TABLE project_trial(
  trial_id           INT       UNSIGNED  NOT NULL AUTO_INCREMENT PRIMARY KEY,
  project_id         MEDIUMINT UNSIGNED  NOT NULL,
  status_id          TINYINT   UNSIGNED  NOT NULL,
  status_change_date TIMESTAMP           NOT NULL,
 CONSTRAINT trial_projid_fk  FOREIGN KEY (project_id) REFERENCES project (project_id),
 CONSTRAINT trial_statid_fk  FOREIGN KEY (status_id)  REFERENCES trial_status (status_id)
)
ENGINE=InnoDB
COMMENT "Tracks the various trial stages for each Amelia's Own project.";


CREATE TABLE inventory(
  inventory_id        MEDIUMINT   UNSIGNED  NOT NULL AUTO_INCREMENT PRIMARY KEY,
  inventory_item_name VARCHAR(100)          NOT NULL,
  product_type_id     SMALLINT    UNSIGNED  NOT NULL,
  package_size_grams  VARCHAR(5)            NOT NULL,
  package_size_oz     VARCHAR(5)            NOT NULL,
  package_type_id     TINYINT     UNSIGNED  NOT NULL,
  material_id         TINYINT     UNSIGNED  NOT NULL,
  manu_id             SMALLINT    UNSIGNED,
  upc                 CHAR(12)              NOT NULL,
 CONSTRAINT inven_upc_uq         UNIQUE (upc),
 CONSTRAINT inven_prodtypeid_fk  FOREIGN KEY (product_type_id) REFERENCES product_type (product_type_id),
 CONSTRAINT inven_pkgtypeid_fk   FOREIGN KEY (package_type_id) REFERENCES package_type (package_type_id),
 CONSTRAINT inven_matid_fk       FOREIGN KEY (material_id)     REFERENCES package_material (material_id),
 CONSTRAINT inven_manuid_fk      FOREIGN KEY (manu_id)         REFERENCES manufacturer (manu_id)
)
ENGINE=InnoDB
COMMENT 'Tracks all current and past inventory sold at Süsse Wurst.';


CREATE TABLE active_inventory(
  active_id MEDIUMINT UNSIGNED  NOT NULL PRIMARY KEY,
  sku       CHAR(9)             NOT NULL,
 CONSTRAINT actinven_activeid_fk FOREIGN KEY (active_id) REFERENCES inventory (inventory_id),
 CONSTRAINT actinven_sku_uq      UNIQUE (sku)
)
ENGINE=InnoDB
COMMENT 'Tracks all current inventory.';


CREATE TABLE disco_reason(
  disco_code        TINYINT     UNSIGNED  NOT NULL AUTO_INCREMENT PRIMARY KEY,
  disco_reason_name VARCHAR(50)           NOT NULL,
  disco_reason_desc VARCHAR(100)          NOT NULL
)
ENGINE=InnoDB
COMMENT 'Tracks various reasons for product discontinuation.';


CREATE TABLE disco_inventory(
  disco_id    MEDIUMINT UNSIGNED  NOT NULL PRIMARY KEY,
  sku         CHAR(9)             NOT NULL,
  disco_date  DATE                NOT NULL,
  disco_code  TINYINT   UNSIGNED  NOT NULL,
 CONSTRAINT disco_discoid_fk FOREIGN KEY (disco_id) REFERENCES inventory (inventory_id),
 CONSTRAINT disco_sku_uq     UNIQUE (sku)
)
ENGINE=InnoDB
COMMENT 'Tracks all discontinued inventory.';


CREATE TABLE ingredient_panel(
  ingred_panel_id  MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  active_id        MEDIUMINT UNSIGNED NOT NULL,
  ingredient_panel TEXT               NOT NULL,
 CONSTRAINT ingredpan_activeid_fk FOREIGN KEY (active_id) REFERENCES active_inventory (active_id) ON DELETE CASCADE,
 FULLTEXT ingredpan_ingreds_ix (ingredient_panel)
)
ENGINE=InnoDB
COMMENT 'Tracks the ingredient panel for each product sold at Süsse Wurst.';


CREATE TABLE vendor(
  vendor_id       SMALLINT     UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  vendor_name     VARCHAR(100)          NOT NULL,
  vendor_address  VARCHAR(100)          NOT NULL,
  vendor_city     VARCHAR(100)          NOT NULL,
  vendor_state    CHAR(2)               NOT NULL,
  vendor_zip_code CHAR(5)               NOT NULL,
  vendor_phone    CHAR(12)              NOT NULL,
  vendor_website  VARCHAR(100)          NOT NULL,
 CONSTRAINT vendor_website_uq UNIQUE (vendor_website),
 CONSTRAINT vendor_name_uq    UNIQUE (vendor_name)
)
ENGINE=InnoDB
COMMENT 'Tracks the various vendors Süsse Wurst orders from.';


CREATE TABLE vendor_contact(
  contact_id    SMALLINT     UNSIGNED      NOT NULL AUTO_INCREMENT PRIMARY KEY,
  vendor_id     SMALLINT     UNSIGNED      NOT NULL,
  contact_fname VARCHAR(50)                NOT NULL,
  contact_lname VARCHAR(50)                NOT NULL,
  contact_phone CHAR(12)                   NOT NULL,
  contact_email VARCHAR(100) DEFAULT NULL,
 CONSTRAINT vendcon_vendorid_fk FOREIGN KEY (vendor_id) REFERENCES vendor (vendor_id),
 CONSTRAINT vendcon_email_uq    UNIQUE (contact_email)
)
ENGINE=InnoDB
COMMENT 'Tracks contact information for vendor representatives.';


CREATE TABLE ingredient_category(
  ingred_cat_id   TINYINT     UNSIGNED  NOT NULL AUTO_INCREMENT PRIMARY KEY,
  ingred_cat_name VARCHAR(50)           NOT NULL
)
ENGINE=InnoDB
COMMENT 'Tracks broad categories for cataloguing in-store ingredients.';


CREATE TABLE store_ingredient(
  store_ingred_id   SMALLINT     UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  store_ingred_name VARCHAR(100)          NOT NULL,
  ingred_cat_id     TINYINT      UNSIGNED NOT NULL,
 CONSTRAINT storeingred_catid_fk FOREIGN KEY (ingred_cat_id) REFERENCES ingredient_category (ingred_cat_id)
)
ENGINE=InnoDB
COMMENT 'Tracks ingredients used for store-made products.';


CREATE TABLE inventory_location(
  loc_id      SMALLINT  UNSIGNED NOT NULL,
  active_id   MEDIUMINT UNSIGNED NOT NULL,
  aisle_num   VARCHAR(2)         NOT NULL,
  aisle_side  CHAR(1)            NOT NULL,
  bay_num     VARCHAR(2)         NOT NULL,
  cubby_num   VARCHAR(2)         NOT NULL,
  row_num     CHAR(1)            NOT NULL,
 PRIMARY KEY (loc_id, active_id),
 CONSTRAINT invenloc_locid_fk    FOREIGN KEY (loc_id)      REFERENCES sw_hr.location (loc_id) ON DELETE CASCADE,
 CONSTRAINT invenloc_activeid_fk FOREIGN KEY (active_id)   REFERENCES active_inventory (active_id)
)
ENGINE=InnoDB
COMMENT 'Tracks the aisle location of each inventory item at any Süsse Wurst store.';


CREATE TABLE inventory_order(
  order_id      INT       UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  dept_id       SMALLINT  UNSIGNED NOT NULL,
  emp_id        MEDIUMINT UNSIGNED NOT NULL,
  order_date    DATETIME           NOT NULL,
 CONSTRAINT order_deptid_fk FOREIGN KEY (dept_id)       REFERENCES sw_hr.department (dept_id)     ON DELETE CASCADE,
 CONSTRAINT order_empid_fk  FOREIGN KEY (emp_id)        REFERENCES sw_hr.active_employee (emp_id) ON DELETE CASCADE
)
ENGINE=InnoDB
COMMENT 'Tracks all orders placed in-store for ingredient supplies.';


CREATE TABLE store_order_item(
  order_id        INT          UNSIGNED NOT NULL,
  store_ingred_id SMALLINT     UNSIGNED NOT NULL,
  vendor_id       SMALLINT     UNSIGNED NOT NULL,
  item_quantity   SMALLINT     UNSIGNED NOT NULL,
  vendor_price    DECIMAL(6,2) NOT NULL,
 PRIMARY KEY (order_id, store_ingred_id),
 CONSTRAINT storeorder_orderid_fk  FOREIGN KEY (order_id)        REFERENCES inventory_order (order_id),
 CONSTRAINT storeorder_ingredid_fk FOREIGN KEY (store_ingred_id) REFERENCES store_ingredient (store_ingred_id),
 CONSTRAINT storeorder_quantity_ck CHECK (item_quantity > 0),
 CONSTRAINT storeorder_price_ck    CHECK (vendor_price > 0.0)
)
ENGINE=InnoDB
COMMENT "Tracks each in-store order's line item.";


CREATE TABLE dist_order_item(
  order_id      INT          UNSIGNED NOT NULL,
  active_id     MEDIUMINT    UNSIGNED NOT NULL,
  vendor_id     SMALLINT     UNSIGNED NOT NULL,
  item_quantity SMALLINT     UNSIGNED NOT NULL,
  vendor_price  DECIMAL(6,2) NOT NULL,
 PRIMARY KEY (order_id, active_id),
 CONSTRAINT distorder_orderid_fk  FOREIGN KEY (order_id)  REFERENCES inventory_order (order_id),
 CONSTRAINT distorder_activeid_fk FOREIGN KEY (active_id) REFERENCES active_inventory (active_id),
 CONSTRAINT distorder_quantity_ck CHECK (item_quantity > 0),
 CONSTRAINT distorder_price_ck    CHECK (vendor_price > 0.0)
)
ENGINE=InnoDB
COMMENT "Tracks each inventory order's line item.";


/*********** V. CREATE HR USER FOR LOGGING INTO GUI APPLICATION ***********/
DROP USER IF EXISTS hr_associate;

CREATE USER hr_associate
IDENTIFIED BY 'wouldyoukindly';

GRANT ALL 
ON sw_hr.*
TO hr_associate;

/*** END OF FILE ***/