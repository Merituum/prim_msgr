-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Maj 03, 2024 at 11:12 AM
-- Wersja serwera: 10.4.28-MariaDB
-- Wersja PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `prim_msgr`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `Users`
--

CREATE TABLE `Users` (
  `ID` int(11) NOT NULL,
  `Login` varchar(50) NOT NULL,
  `Haslo` varchar(100) NOT NULL,
  `PytaniePomocnicze` varchar(255) NOT NULL,
  `OdpowiedzNaPytanie` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

--
-- Dumping data for table `Users`
--

INSERT INTO `Users` (`ID`, `Login`, `Haslo`, `PytaniePomocnicze`, `OdpowiedzNaPytanie`) VALUES
(1, 'admin', 'admin', 'admin?', 'admin'),
(2, 'uzyt_1', 'uzytkownik', 'uzyt1', 'yzut'),
(3, 'beachlover', 'SunSand123', 'Jakie jest twoje ulubione miejsce na plaży?', 'Hawaje'),
(4, 'musicaddict', 'Melody456', 'Jaki jest twój ulubiony gatunek muzyczny?', 'Pop'),
(5, 'traveler23', 'Adventure123', 'Jak wiele krajów odwiedziłeś?', '20'),
(6, 'foodie', 'Taste123', 'Jaka jest twoja ulubiona potrawa?', 'Pizza'),
(7, 'movieaddict', 'Cinema789', 'Jaki jest twój ulubiony film?', 'Incepcja'),
(8, 'fitnesslover', 'FitLife123', 'Jak często ćwiczysz?', 'Codziennie'),
(9, 'animalenthusiast', 'Animal123', 'Które zwierzę jest twoim ulubionym?', 'Pies'),
(10, 'booklover', 'Bookworm123', 'Jaki jest twój ulubiony tytuł książki?', 'Harry Potter'),
(11, 'natureenthusiast', 'Nature123', 'Jaki jest twój ulubiony gatunek drzewa?', 'Dąb'),
(12, 'artfanatic', 'Art123', 'Kto jest twoim ulubionym artystą?', 'Vincent van Gogh'),
(13, 'photographylife', 'Photo123', 'Jaki jest twój ulubiony obiektyw?', '50mm'),
(14, 'coffeelover', 'Caffeine123', 'Jaki jest twój ulubiony rodzaj kawy?', 'Espresso'),
(15, 'gamer', 'Gaming123', 'Jaka jest twoja ulubiona gra?', 'The Witcher 3'),
(16, 'gardeninglover', 'Garden123', 'Jaki jest twój ulubiony rodzaj kwiatów?', 'Tulipany'),
(17, 'techenthusiast', 'Techie123', 'Jaki jest twój ulubiony gadżet?', 'Smartwatch'),
(18, 'yogalover', 'Yoga123', 'Jakie jest twoje ulubione miejsce do praktyki jogi?', 'Park'),
(19, 'craftlover', 'Crafty123', 'Jaki jest twój ulubiony rodzaj rękodzieła?', 'Decoupage'),
(20, 'hikinglover', 'Hike456', 'Jaki jest twój ulubiony szlak?', 'Pacific Crest Trail'),
(21, 'codinglover', 'Code456', 'Jaki jest twój ulubiony język programowania?', 'Java'),
(22, 'beautyenthusiast', 'Beauty123', 'Jaki jest twój ulubiony kosmetyk?', 'Pomadka'),
(23, 'fashionlover', 'Fashion123', 'Jaki jest twój ulubiony kolor ubrania?', 'Czarny'),
(24, 'DIYlover', 'DIY123', 'Jaki jest twój ulubiony projekt DIY?', 'Ozdobne poduszki'),
(25, 'wineenthusiast', 'Wine123', 'Jaki jest twój ulubiony gatunek wina?', 'Czerwone'),
(26, 'surfingenthusiast', 'Surf123', 'Jaki jest twój ulubiony rodzaj fali?', 'Tubing'),
(27, 'danceenthusiast', 'Dance123', 'Jaki jest twój ulubiony rodzaj tańca?', 'Tango'),
(28, 'carlover', 'Car123', 'Jaki jest twój ulubiony model samochodu?', 'Mustang'),
(29, 'runninglover', 'Run123', 'Jaki jest twój ulubiony dystans do biegu?', '10 km'),
(30, 'skiingenthusiast', 'Ski123', 'Jaki jest twój ulubiony kurort narciarski?', 'Whistler'),
(31, 'boardgameenthusiast', 'Board123', 'Jaki jest twój ulubiony rodzaj gry planszowej?', 'Catan'),
(32, 'scubadivingenthusiast', 'Dive123', 'Jaki jest twój ulubiony gatunek ryby do nurkowania?', 'Nemo'),
(33, 'cookinglover', 'Cook123', 'Jaki jest twój ulubiony przepis?', 'Lasagne'),
(34, 'backpackinglover', 'Pack123', 'Jaki jest twój ulubiony kraj do plecaka?', 'Tajlandia'),
(35, 'mountainbikingenthusiast', 'Bike123', 'Jaki jest twój ulubiony szlak rowerowy?', 'Downhill'),
(36, 'astronomyenthusiast', 'Space123', 'Co jest twoim ulubionym obiektem do obserwacji w kosmosie?', 'Księżyc'),
(37, 'karateenthusiast', 'Karate123', 'Jaki jest twój stopień karate?', 'Czarny'),
(38, 'surfinglover', 'Surf456', 'Jaki jest twój ulubiony rodzaj deski do surfowania?', 'Longboard'),
(39, 'birdwatcher', 'Bird123', 'Jaki jest twój ulubiony gatunek ptaka?', 'Sowa'),
(40, 'volleyballenthusiast', 'Volley123', 'Jaki jest twój ulubiony rodzaj zagrywki w siatkówce?', 'Placemats'),
(41, 'sailingenthusiast', 'Sail123', 'Jaki jest twój ulubiony rodzaj jachtu?', 'Kuter'),
(42, 'paintinglover', 'Paint123', 'Jaki jest twój ulubiony rodzaj farby?', 'Akryl'),
(43, 'golfenthusiast', 'Golf123', 'Jaki jest twój ulubiony pole golfowe?', 'Augusta National'),
(44, 'tennislover', 'Tennis123', 'Jaki jest twój ulubiony rodzaj rakiety do tenisa?', 'Wilson'),
(45, 'basketballfanatic', 'Basket123', 'Jaki jest twój ulubiony zespół NBA?', 'Los Angeles Lakers'),
(46, 'skydivingenthusiast', 'Skydive123', 'Jaki jest twój ulubiony rodzaj spadochronu?', 'Tandemowy'),
(47, 'chessenthusiast', 'Chess123', 'Jaki jest twój ulubiony otwarcie w szachach?', 'Sycylijskie'),
(48, 'surfingfanatic', 'Surf789', 'Jaki jest twój ulubiony spot surfowania?', 'Banzai Pipeline'),
(49, 'snowboardinglover', 'Snowboard123', 'Jaki jest twój ulubiony rodzaj narty?', 'Freestyle'),
(50, 'baseballenthusiast', 'Baseball123', 'Jaki jest twój ulubiony stadion MLB?', 'Wrigley Field'),
(51, 'snorkelingenthusiast', 'Snorkel123', 'Jaki jest twój ulubiony gatunek ryby do snorkelingu?', 'Ryba-papuga'),
(52, 'kayakinglover', 'Kayak123', 'Jaki jest twój ulubiony rodzaj kajaka?', 'Sit-on-top'),
(53, 'windsurfingenthusiast', 'Windsurf123', 'Jaki jest twój ulubiony rodzaj żagla do windsurfingu?', 'Skwirrel'),
(54, 'pokerenthusiast', 'Poker123', 'Jaki jest twój ulubiony rodzaj pokera?', 'Texas Hold\'em'),
(55, 'cyclingenthusiast', 'Cycle123', 'Jaki jest twój ulubiony dystans do jazdy na rowerze?', '50 km'),
(56, 'hockeyfanatic', 'Hockey123', 'Jaki jest twój ulubiony zespół NHL?', 'Montreal Canadiens'),
(57, 'whalewatcher', 'Whale123', 'Jaki jest twój ulubiony gatunek wieloryba do obserwacji?', 'Błękitny'),
(58, 'raftingenthusiast', 'Raft123', 'Jaki jest twój ulubiony nurt do spływu?', 'Szalony'),
(59, 'climbingenthusiast', 'Climb123', 'Jaki jest twój ulubiony rodzaj skały do wspinaczki?', 'Granit'),
(60, 'bowlingenthusiast', 'Bowl123', 'Jaki jest twój ulubiony rodzaj kręgli?', 'Kręgle amerykańskie'),
(61, 'boxingenthusiast', 'Box123', 'Jaki jest twój ulubiony styl walki bokserskiej?', 'Kontratak'),
(62, 'soccernut', 'Soccer123', 'Jaki jest twój ulubiony klub piłkarski?', 'Real Madrid'),
(63, 'kitesurfingenthusiast', 'Kite123', 'Jaki jest twój ulubiony rodzaj latawca do kitesurfingu?', 'C-kite'),
(64, 'runningenthusiast', 'Run456', 'Jaki jest twój ulubiony dystans maratonu?', '42 km'),
(65, 'skateboardingenthusiast', 'Skate123', 'Jaki jest twój ulubiony rodzaj deski do skateboardingu?', 'Longboard'),
(66, 'basketballlover', 'Basketball123', 'Jaki jest twój ulubiony rodzaj kosza?', 'Trojka'),
(67, 'fishingenthusiast', 'Fish123', 'Jaki jest twój ulubiony gatunek ryby do wędkowania?', 'Pstrąg'),
(68, 'musiclover987', 'Melody987', 'Jakie jest twoje ulubione miejsce na koncerty?', 'Arena'),
(69, 'traveller456', 'Travel456', 'Jak wiele kontynentów odwiedziłeś?', '3'),
(70, 'foodlover123', 'Food123', 'Jaka jest twoja ulubiona potrawa kuchni śródziemnomorskiej?', 'Paella'),
(71, 'moviefan456', 'Movie456', 'Jaki jest twój ulubiony gatunek filmowy?', 'Komedia'),
(72, 'fitnessjunkie789', 'Fitness789', 'Jak często ćwiczysz?', '5 razy w tygodniu'),
(73, 'animalenthusiast123', 'Animal123', 'Które zwierzę jest twoim ulubionym?', 'Kot'),
(74, 'bookworm789', 'Book789', 'Jaki jest twój ulubiony autor?', 'J.K. Rowling'),
(75, 'naturelover456', 'Nature456', 'Jaki jest twój ulubiony park narodowy?', 'Yellowstone'),
(76, 'artlover789', 'Art789', 'Jakiego koloru używasz najczęściej w swoich obrazach?', 'Niebieski'),
(77, 'photographylover123', 'Photo123', 'Jaki jest twój ulubiony rodzaj obiektywu?', '50mm f/1.8'),
(78, 'coffeefanatic789', 'Coffee789', 'Jaki jest twój ulubiony gatunek kawy?', 'Latte'),
(79, 'gamer456', 'Gamer456', 'Jaka jest twoja ulubiona platforma do gier?', 'PC'),
(80, 'gardeningenthusiast789', 'Garden789', 'Jaki jest twój ulubiony kwiat?', 'Róża'),
(81, 'techlover123', 'Tech123', 'Jaki jest twój ulubiony gadżet elektroniczny?', 'Smartfon'),
(82, 'yogafanatic789', 'Yoga789', 'Jaka jest twoja ulubiona pozycja?', 'Dogi'),
(83, 'craftlover456', 'Craft456', 'Jaki jest twój ulubiony rodzaj rękodzieła?', 'Decoupage'),
(84, 'hikingenthusiast789', 'Hiking789', 'Jaki jest twój ulubiony szlak?', 'Camino de Santiago'),
(85, 'codingenthusiast789', 'Coding789', 'Jaki jest twój ulubiony język programowania?', 'C++'),
(86, 'beautylover123', 'Beauty123', 'Jaki jest twój ulubiony kosmetyk?', 'Puder'),
(87, 'fashionenthusiast789', 'Fashion789', 'Jaki jest twój ulubiony gatunek mody?', 'Streetwear'),
(88, 'DIYfanatic123', 'DIY123', 'Jaki jest twój ulubiony projekt DIY?', 'Stół z palet'),
(89, 'winelover456', 'Wine456', 'Jaki jest twój ulubiony rodzaj wina?', 'Czerwone'),
(90, 'surfingfan789', 'Surf789', 'Jaki jest twój ulubiony rodzaj fali do surfowania?', 'Tubing'),
(91, 'dancelover123', 'Dance123', 'Jaki jest twój ulubiony rodzaj tańca?', 'Hip-hop'),
(92, 'carfanatic789', 'Car789', 'Jaki jest twój ulubiony model samochodu?', 'Audi'),
(93, 'runningenthusiast456', 'Running456', 'Jaki jest twój ulubiony dystans do biegu?', 'Półmaraton'),
(94, 'skiinglover789', 'Ski789', 'Jaki jest twój ulubiony kurort narciarski?', 'Aspen'),
(95, 'boardgamefanatic123', 'Board123', 'Jaki jest twój ulubiony rodzaj gry planszowej?', 'Monopoly'),
(96, 'scubadivingenthusiast789', 'Scuba789', 'Jaki jest twój ulubiony gatunek ryby do nurkowania?', 'Rekin'),
(97, 'cookingenthusiast456', 'Cooking456', 'Jaki jest twój ulubiony przepis kulinarny?', 'Tiramisu'),
(98, 'backpackingfanatic789', 'Backpack789', 'Jaki jest twój ulubiony kraj do plecaka?', 'Nowa Zelandia'),
(99, 'mountainbikinglover123', 'Mountain123', 'Jaki jest twój ulubiony szlak rowerowy?', 'Whistler Bike Park'),
(100, 'astronomylover789', 'Space789', 'Co jest twoim ulubionym obiektem do obserwacji w kosmosie?', 'Mars'),
(101, 'karatefanatic123', 'Karate123', 'Jaki jest twój stopień karate?', 'Czarny'),
(102, 'surfinglover456', 'Surf456', 'Jaki jest twój ulubiony rodzaj deski do surfowania?', 'Shortboard'),
(103, 'birdwatcher789', 'Bird789', 'Jaki jest twój ulubiony gatunek ptaka?', 'Sokół'),
(104, 'volleyballenthusiast456', 'Volley456', 'Jaki jest twój ulubiony rodzaj zagrywki w siatkówce?', 'Atak'),
(105, 'sailingenthusiast789', 'Sailing789', 'Jaki jest twój ulubiony rodzaj jachtu?', 'Katamaran'),
(106, 'paintingenthusiast123', 'Painting123', 'Jaki jest twój ulubiony rodzaj farby?', 'Olejna'),
(107, 'golflover789', 'Golf789', 'Jaki jest twój ulubiony klub golfowy?', 'Pebble Beach'),
(108, 'tennisenthusiast456', 'Tennis456', 'Jaki jest twój ulubiony rodzaj rakietki do tenisa?', 'Head'),
(109, 'basketballfanatic789', 'Basketball789', 'Jaki jest twój ulubiony zespół NCAA?', 'Duke Blue Devils'),
(110, 'skydivingenthusiast789', 'Skydive789', 'Jaki jest twój ulubiony rodzaj spadochronu?', 'Skrzydlaty'),
(111, 'chessenthusiast456', 'Chess456', 'Jaki jest twój ulubiony ruch otwarcia w szachach?', 'Siciliańska obrona'),
(112, 'surfingfanatic789', 'Surfing789', 'Jaki jest twój ulubiony spot surfowania?', 'Pipeline'),
(113, 'snowboardinglover123', 'Snowboard123', 'Jaki jest twój ulubiony rodzaj deski do snowboardingu?', 'Freestyle'),
(114, 'baseballenthusiast789', 'Baseball789', 'Jaki jest twój ulubiony stadion MLB?', 'Dodger Stadium'),
(115, 'snorkelingenthusiast456', 'Snorkel456', 'Jaki jest twój ulubiony gatunek ryby do snorkelingu?', 'Papuga'),
(116, 'kayakinglover789', 'Kayak789', 'Jaki jest twój ulubiony rodzaj kajaka?', 'Kajak turystyczny'),
(117, 'windsurfingenthusiast456', 'Windsurf456', 'Jaki jest twój ulubiony rodzaj żagla do windsurfingu?', 'Foil'),
(118, 'pokerenthusiast789', 'Poker789', 'Jaki jest twój ulubiony rodzaj pokera?', 'Omaha'),
(119, 'cyclingenthusiast456', 'Cycle456', 'Jaki jest twój ulubiony dystans do jazdy na rowerze?', '100 km'),
(120, 'hockeyfanatic789', 'Hockey789', 'Jaki jest twój ulubiony zespół NHL?', 'Chicago Blackhawks'),
(121, 'whalewatcher456', 'Whale456', 'Jaki jest twój ulubiony gatunek wieloryba do obserwacji?', 'Orka'),
(122, 'raftingenthusiast789', 'Raft789', 'Jaki jest twój ulubiony nurt do spływu?', 'Bezimienny'),
(123, 'climbingenthusiast456', 'Climb456', 'Jaki jest twój ulubiony rodzaj skały do wspinaczki?', 'Wapienna'),
(124, 'bowlingenthusiast789', 'Bowl789', 'Jaki jest twój ulubiony rodzaj kręgli?', 'Kręgle angielskie'),
(125, 'boxingenthusiast456', 'Boxing456', 'Jaki jest twój ulubiony styl walki bokserskiej?', 'Kontratak'),
(126, 'soccernut789', 'Soccer789', 'Jaki jest twój ulubiony klub piłkarski?', 'Manchester United'),
(127, 'kitesurfingenthusiast456', 'Kite456', 'Jaki jest twój ulubiony rodzaj latawca do kitesurfingu?', 'Foil'),
(128, 'runningenthusiast789', 'Run789', 'Jaki jest twój ulubiony dystans maratonu?', '50 km'),
(129, 'skateboardingenthusiast456', 'Skate456', 'Jaki jest twój ulubiony rodzaj deski do skateboardingu?', 'Cruiser'),
(130, 'basketballlover789', 'Basket789', 'Jaki jest twój ulubiony rodzaj kosza?', 'Wyzwanie'),
(131, 'fishingenthusiast456', 'Fish456', 'Jaki jest twój ulubiony gatunek ryby do wędkowania?', 'Sum');

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Users`
--
ALTER TABLE `Users`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=132;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
