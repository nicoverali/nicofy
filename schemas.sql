CREATE TABLE nicofy_links (
  id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
  new_link VARCHAR(255) NOT NULL,
  old_link VARCHAR(255) NOT NULL,
  user_id VARCHAR(255) NOT NULL
);

CREATE TABLE nicofy_users (
  user_id VARCHAR(255) NOT NULL PRIMARY KEY
);
