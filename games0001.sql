--
-- Create model Collection
--
CREATE TABLE `games_collection` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `igdb_id` bigint UNSIGNED NOT NULL UNIQUE CHECK (`igdb_id` >= 0), `name` varchar(255) NOT NULL, `slug` varchar(255) NOT NULL);
--
-- Create model Company
--
CREATE TABLE `games_company` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `igdb_id` bigint UNSIGNED NOT NULL UNIQUE CHECK (`igdb_id` >= 0), `name` varchar(255) NOT NULL, `igdb_updated_at` datetime(6) NULL);
--
-- Create model Franchise
--
CREATE TABLE `games_franchise` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `igdb_id` bigint UNSIGNED NOT NULL UNIQUE CHECK (`igdb_id` >= 0), `name` varchar(255) NOT NULL, `slug` varchar(255) NOT NULL);
--
-- Create model GameMode
--
CREATE TABLE `games_gamemode` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `igdb_id` bigint UNSIGNED NOT NULL UNIQUE CHECK (`igdb_id` >= 0), `name` varchar(255) NOT NULL, `slug` varchar(255) NOT NULL);
--
-- Create model GameStatus
--
CREATE TABLE `games_gamestatus` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(255) NOT NULL, `description` longtext NOT NULL, `image` varchar(100) NOT NULL);
--
-- Create model Genre
--
CREATE TABLE `games_genre` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `igdb_id` bigint UNSIGNED NOT NULL UNIQUE CHECK (`igdb_id` >= 0), `name` varchar(255) NOT NULL, `slug` varchar(255) NOT NULL);
--
-- Create model IGDBSyncStatus
--
CREATE TABLE `games_igdbsyncstatus` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `last_updated_at` datetime(6) NULL, `last_updated_ids` json NOT NULL);
--
-- Create model Keyword
--
CREATE TABLE `games_keyword` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `igdb_id` bigint UNSIGNED NOT NULL UNIQUE CHECK (`igdb_id` >= 0), `name` varchar(255) NOT NULL, `slug` varchar(255) NOT NULL);
--
-- Create model Platform
--
CREATE TABLE `games_platform` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `igdb_id` bigint UNSIGNED NOT NULL UNIQUE CHECK (`igdb_id` >= 0), `name` varchar(255) NOT NULL, `slug` varchar(255) NOT NULL, `abbreviation` varchar(255) NOT NULL, `alternative_name` varchar(255) NOT NULL);
--
-- Create model PlayerPerspective
--
CREATE TABLE `games_playerperspective` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `igdb_id` bigint UNSIGNED NOT NULL UNIQUE CHECK (`igdb_id` >= 0), `name` varchar(255) NOT NULL, `slug` varchar(255) NOT NULL);
--
-- Create model RatingCategory
--
CREATE TABLE `games_ratingcategory` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(255) NOT NULL, `key` varchar(50) NOT NULL UNIQUE);
--
-- Create model RatingType
--
CREATE TABLE `games_ratingtype` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(50) NOT NULL, `image` varchar(100) NOT NULL, `weight` smallint UNSIGNED NOT NULL CHECK (`weight` >= 0), `color` varchar(20) NOT NULL, `category_rating_name` varchar(50) NULL, `category_rating_description` longtext NULL);
--
-- Create model Theme
--
CREATE TABLE `games_theme` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `igdb_id` bigint UNSIGNED NOT NULL UNIQUE CHECK (`igdb_id` >= 0), `name` varchar(255) NOT NULL, `slug` varchar(255) NOT NULL);
--
-- Create model Game
--
CREATE TABLE `games_game` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `igdb_id` bigint UNSIGNED NULL UNIQUE CHECK (`igdb_id` >= 0), `name` varchar(255) NOT NULL, `description` longtext NOT NULL, `released` date NULL, `igdb_updated_at` datetime(6) NULL, `cover_url` varchar(200) NULL, `story_line` longtext NULL, `hypes` integer NULL, `igdb_rating` double precision NULL, `igdb_rating_count` integer NULL, `total_rating` double precision NULL, `total_rating_count` integer NULL, `igdb_url` varchar(200) NULL);
CREATE TABLE `games_game_collections` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `game_id` bigint NOT NULL, `collection_id` bigint NOT NULL);
CREATE TABLE `games_game_developer` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `game_id` bigint NOT NULL, `company_id` bigint NOT NULL);
CREATE TABLE `games_game_franchises` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `game_id` bigint NOT NULL, `franchise_id` bigint NOT NULL);
CREATE TABLE `games_game_publisher` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `game_id` bigint NOT NULL, `company_id` bigint NOT NULL);
CREATE TABLE `games_game_similar_games` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `from_game_id` bigint NOT NULL, `to_game_id` bigint NOT NULL);
CREATE TABLE `games_game_game_modes` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `game_id` bigint NOT NULL, `gamemode_id` bigint NOT NULL);
CREATE TABLE `games_game_genres` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `game_id` bigint NOT NULL, `genre_id` bigint NOT NULL);
CREATE TABLE `games_game_keywords` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `game_id` bigint NOT NULL, `keyword_id` bigint NOT NULL);
CREATE TABLE `games_game_platforms` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `game_id` bigint NOT NULL, `platform_id` bigint NOT NULL);
CREATE TABLE `games_game_player_perspectives` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `game_id` bigint NOT NULL, `playerperspective_id` bigint NOT NULL);
CREATE TABLE `games_game_themes` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `game_id` bigint NOT NULL, `theme_id` bigint NOT NULL);
--
-- Create model GameTimeToBeat
--
CREATE TABLE `games_gametimetobeat` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `main_story` numeric(5, 2) NULL, `main_sides` numeric(5, 2) NULL, `completion` numeric(5, 2) NULL, `game_id` bigint NOT NULL UNIQUE);
--
-- Create model GameOverallRating
--
CREATE TABLE `games_gameoverallrating` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `updated_at` datetime(6) NOT NULL, `game_id` bigint NOT NULL, `user_id` integer NOT NULL, `rating_type_id` bigint NOT NULL);
--
-- Create model GameCategoryRating
--
CREATE TABLE `games_gamecategoryrating` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `updated_at` datetime(6) NOT NULL, `game_id` bigint NOT NULL, `user_id` integer NOT NULL, `category_id` bigint NOT NULL, `rating_type_id` bigint NOT NULL);
--
-- Create model UserLibrary
--
CREATE TABLE `games_userlibrary` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `added` datetime(6) NOT NULL, `game_id` bigint NOT NULL, `status_id` bigint NULL, `user_id` integer NOT NULL);
--
-- Create model WishList
--
CREATE TABLE `games_wishlist` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `added` datetime(6) NOT NULL, `game_id` bigint NOT NULL, `user_id` integer NOT NULL);
CREATE INDEX `games_collection_slug_28d5ea83` ON `games_collection` (`slug`);
CREATE INDEX `games_franchise_slug_f7673d7c` ON `games_franchise` (`slug`);
CREATE INDEX `games_gamemode_slug_27f65632` ON `games_gamemode` (`slug`);
CREATE INDEX `games_genre_slug_820ec875` ON `games_genre` (`slug`);
CREATE INDEX `games_keyword_slug_c79a3c4a` ON `games_keyword` (`slug`);
CREATE INDEX `games_platform_slug_3baba989` ON `games_platform` (`slug`);
CREATE INDEX `games_playerperspective_slug_35e45e47` ON `games_playerperspective` (`slug`);
CREATE INDEX `games_theme_slug_365877c4` ON `games_theme` (`slug`);
CREATE INDEX `games_game_igdb_rating_644d6f14` ON `games_game` (`igdb_rating`);
CREATE INDEX `games_game_total_rating_3ed464f7` ON `games_game` (`total_rating`);
ALTER TABLE `games_game_collections` ADD CONSTRAINT `games_game_collections_game_id_collection_id_b7eef699_uniq` UNIQUE (`game_id`, `collection_id`);
ALTER TABLE `games_game_collections` ADD CONSTRAINT `games_game_collections_game_id_80709146_fk_games_game_id` FOREIGN KEY (`game_id`) REFERENCES `games_game` (`id`);
ALTER TABLE `games_game_collections` ADD CONSTRAINT `games_game_collectio_collection_id_85dbff75_fk_games_col` FOREIGN KEY (`collection_id`) REFERENCES `games_collection` (`id`);
ALTER TABLE `games_game_developer` ADD CONSTRAINT `games_game_developer_game_id_company_id_242f7a95_uniq` UNIQUE (`game_id`, `company_id`);
ALTER TABLE `games_game_developer` ADD CONSTRAINT `games_game_developer_game_id_bb3cf011_fk_games_game_id` FOREIGN KEY (`game_id`) REFERENCES `games_game` (`id`);
ALTER TABLE `games_game_developer` ADD CONSTRAINT `games_game_developer_company_id_d9fed426_fk_games_company_id` FOREIGN KEY (`company_id`) REFERENCES `games_company` (`id`);
ALTER TABLE `games_game_franchises` ADD CONSTRAINT `games_game_franchises_game_id_franchise_id_b3e8fcca_uniq` UNIQUE (`game_id`, `franchise_id`);
ALTER TABLE `games_game_franchises` ADD CONSTRAINT `games_game_franchises_game_id_1d1eecf9_fk_games_game_id` FOREIGN KEY (`game_id`) REFERENCES `games_game` (`id`);
ALTER TABLE `games_game_franchises` ADD CONSTRAINT `games_game_franchise_franchise_id_c7de87aa_fk_games_fra` FOREIGN KEY (`franchise_id`) REFERENCES `games_franchise` (`id`);
ALTER TABLE `games_game_publisher` ADD CONSTRAINT `games_game_publisher_game_id_company_id_c3dceeed_uniq` UNIQUE (`game_id`, `company_id`);
ALTER TABLE `games_game_publisher` ADD CONSTRAINT `games_game_publisher_game_id_faee59a2_fk_games_game_id` FOREIGN KEY (`game_id`) REFERENCES `games_game` (`id`);
ALTER TABLE `games_game_publisher` ADD CONSTRAINT `games_game_publisher_company_id_ba540769_fk_games_company_id` FOREIGN KEY (`company_id`) REFERENCES `games_company` (`id`);
ALTER TABLE `games_game_similar_games` ADD CONSTRAINT `games_game_similar_games_from_game_id_to_game_id_9ee79682_uniq` UNIQUE (`from_game_id`, `to_game_id`);
ALTER TABLE `games_game_similar_games` ADD CONSTRAINT `games_game_similar_games_from_game_id_2fd91655_fk_games_game_id` FOREIGN KEY (`from_game_id`) REFERENCES `games_game` (`id`);
ALTER TABLE `games_game_similar_games` ADD CONSTRAINT `games_game_similar_games_to_game_id_c566dd75_fk_games_game_id` FOREIGN KEY (`to_game_id`) REFERENCES `games_game` (`id`);
ALTER TABLE `games_game_game_modes` ADD CONSTRAINT `games_game_game_modes_game_id_gamemode_id_217c6a3c_uniq` UNIQUE (`game_id`, `gamemode_id`);
ALTER TABLE `games_game_game_modes` ADD CONSTRAINT `games_game_game_modes_game_id_67a75e21_fk_games_game_id` FOREIGN KEY (`game_id`) REFERENCES `games_game` (`id`);
ALTER TABLE `games_game_game_modes` ADD CONSTRAINT `games_game_game_modes_gamemode_id_c4452014_fk_games_gamemode_id` FOREIGN KEY (`gamemode_id`) REFERENCES `games_gamemode` (`id`);
ALTER TABLE `games_game_genres` ADD CONSTRAINT `games_game_genres_game_id_genre_id_acd9b437_uniq` UNIQUE (`game_id`, `genre_id`);
ALTER TABLE `games_game_genres` ADD CONSTRAINT `games_game_genres_game_id_9b3d4740_fk_games_game_id` FOREIGN KEY (`game_id`) REFERENCES `games_game` (`id`);
ALTER TABLE `games_game_genres` ADD CONSTRAINT `games_game_genres_genre_id_8d3275a8_fk_games_genre_id` FOREIGN KEY (`genre_id`) REFERENCES `games_genre` (`id`);
ALTER TABLE `games_game_keywords` ADD CONSTRAINT `games_game_keywords_game_id_keyword_id_4547e9a8_uniq` UNIQUE (`game_id`, `keyword_id`);
ALTER TABLE `games_game_keywords` ADD CONSTRAINT `games_game_keywords_game_id_50bc27f4_fk_games_game_id` FOREIGN KEY (`game_id`) REFERENCES `games_game` (`id`);
ALTER TABLE `games_game_keywords` ADD CONSTRAINT `games_game_keywords_keyword_id_f6aebc17_fk_games_keyword_id` FOREIGN KEY (`keyword_id`) REFERENCES `games_keyword` (`id`);
ALTER TABLE `games_game_platforms` ADD CONSTRAINT `games_game_platforms_game_id_platform_id_f955cb81_uniq` UNIQUE (`game_id`, `platform_id`);
ALTER TABLE `games_game_platforms` ADD CONSTRAINT `games_game_platforms_game_id_450e9ce5_fk_games_game_id` FOREIGN KEY (`game_id`) REFERENCES `games_game` (`id`);
ALTER TABLE `games_game_platforms` ADD CONSTRAINT `games_game_platforms_platform_id_317461e9_fk_games_platform_id` FOREIGN KEY (`platform_id`) REFERENCES `games_platform` (`id`);
ALTER TABLE `games_game_player_perspectives` ADD CONSTRAINT `games_game_player_perspe_game_id_playerperspectiv_24566959_uniq` UNIQUE (`game_id`, `playerperspective_id`);
ALTER TABLE `games_game_player_perspectives` ADD CONSTRAINT `games_game_player_perspectives_game_id_08de9e9b_fk_games_game_id` FOREIGN KEY (`game_id`) REFERENCES `games_game` (`id`);
ALTER TABLE `games_game_player_perspectives` ADD CONSTRAINT `games_game_player_pe_playerperspective_id_697e9055_fk_games_pla` FOREIGN KEY (`playerperspective_id`) REFERENCES `games_playerperspective` (`id`);
ALTER TABLE `games_game_themes` ADD CONSTRAINT `games_game_themes_game_id_theme_id_ea4fef46_uniq` UNIQUE (`game_id`, `theme_id`);
ALTER TABLE `games_game_themes` ADD CONSTRAINT `games_game_themes_game_id_36243178_fk_games_game_id` FOREIGN KEY (`game_id`) REFERENCES `games_game` (`id`);
ALTER TABLE `games_game_themes` ADD CONSTRAINT `games_game_themes_theme_id_d58eb271_fk_games_theme_id` FOREIGN KEY (`theme_id`) REFERENCES `games_theme` (`id`);
ALTER TABLE `games_gametimetobeat` ADD CONSTRAINT `games_gametimetobeat_game_id_94a14a3c_fk_games_game_id` FOREIGN KEY (`game_id`) REFERENCES `games_game` (`id`);
ALTER TABLE `games_gameoverallrating` ADD CONSTRAINT `games_gameoverallrating_game_id_user_id_417a01bb_uniq` UNIQUE (`game_id`, `user_id`);
ALTER TABLE `games_gameoverallrating` ADD CONSTRAINT `games_gameoverallrating_game_id_d7900c34_fk_games_game_id` FOREIGN KEY (`game_id`) REFERENCES `games_game` (`id`);
ALTER TABLE `games_gameoverallrating` ADD CONSTRAINT `games_gameoverallrating_user_id_745b5b82_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `games_gameoverallrating` ADD CONSTRAINT `games_gameoverallrat_rating_type_id_8d328fbd_fk_games_rat` FOREIGN KEY (`rating_type_id`) REFERENCES `games_ratingtype` (`id`);
ALTER TABLE `games_gamecategoryrating` ADD CONSTRAINT `games_gamecategoryrating_game_id_user_id_category_f1a8d771_uniq` UNIQUE (`game_id`, `user_id`, `category_id`);
ALTER TABLE `games_gamecategoryrating` ADD CONSTRAINT `games_gamecategoryrating_game_id_a486cd98_fk_games_game_id` FOREIGN KEY (`game_id`) REFERENCES `games_game` (`id`);
ALTER TABLE `games_gamecategoryrating` ADD CONSTRAINT `games_gamecategoryrating_user_id_e7c7a57e_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `games_gamecategoryrating` ADD CONSTRAINT `games_gamecategoryra_category_id_50cf71e4_fk_games_rat` FOREIGN KEY (`category_id`) REFERENCES `games_ratingcategory` (`id`);
ALTER TABLE `games_gamecategoryrating` ADD CONSTRAINT `games_gamecategoryra_rating_type_id_3d401e25_fk_games_rat` FOREIGN KEY (`rating_type_id`) REFERENCES `games_ratingtype` (`id`);
ALTER TABLE `games_userlibrary` ADD CONSTRAINT `games_userlibrary_user_id_game_id_5423e6ab_uniq` UNIQUE (`user_id`, `game_id`);
ALTER TABLE `games_userlibrary` ADD CONSTRAINT `games_userlibrary_game_id_ccd919b5_fk_games_game_id` FOREIGN KEY (`game_id`) REFERENCES `games_game` (`id`);
ALTER TABLE `games_userlibrary` ADD CONSTRAINT `games_userlibrary_status_id_f22570e9_fk_games_gamestatus_id` FOREIGN KEY (`status_id`) REFERENCES `games_gamestatus` (`id`);
ALTER TABLE `games_userlibrary` ADD CONSTRAINT `games_userlibrary_user_id_1d086e7e_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `games_wishlist` ADD CONSTRAINT `games_wishlist_user_id_game_id_a527328a_uniq` UNIQUE (`user_id`, `game_id`);
ALTER TABLE `games_wishlist` ADD CONSTRAINT `games_wishlist_game_id_48a8f8ae_fk_games_game_id` FOREIGN KEY (`game_id`) REFERENCES `games_game` (`id`);
ALTER TABLE `games_wishlist` ADD CONSTRAINT `games_wishlist_user_id_acb1e282_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
