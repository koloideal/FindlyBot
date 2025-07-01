-- Инициализация базы данных FindlyBot
USE FindlyBot;

-- Создание таблиц (если они не существуют)
CREATE TABLE IF NOT EXISTS users_config(
    username VARCHAR(50) NOT NULL UNIQUE, 
    only_new VARCHAR(3), 
    max_size INTEGER, 
    name_filter VARCHAR(3), 
    price_filter VARCHAR(3), 
    language VARCHAR(2)
);

CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER NOT NULL UNIQUE, 
    first_name VARCHAR(50), 
    username VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS banned_users(
    username VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS admins(
    username VARCHAR(50) NOT NULL
);

-- Предоставление прав пользователю findlybot_user
GRANT ALL PRIVILEGES ON FindlyBot.* TO 'findlybot_user'@'%';
FLUSH PRIVILEGES; 