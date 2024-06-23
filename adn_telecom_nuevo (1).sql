-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 23-06-2024 a las 20:50:31
-- Versión del servidor: 10.4.25-MariaDB
-- Versión de PHP: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `adn_telecom_nuevo`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `componentes`
--

CREATE TABLE `componentes` (
  `ID` int(11) NOT NULL,
  `EQUIPO` varchar(100) NOT NULL,
  `MODELO` varchar(100) NOT NULL,
  `MARCA` varchar(100) NOT NULL,
  `COSTO` float NOT NULL,
  `Velocidad_Red` int(11) NOT NULL,
  `Year` int(11) NOT NULL,
  `Estructura_Red` int(11) NOT NULL,
  `Nro_Puertos` int(11) NOT NULL,
  `approval_Index` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `componentes`
--

INSERT INTO `componentes` (`ID`, `EQUIPO`, `MODELO`, `MARCA`, `COSTO`, `Velocidad_Red`, `Year`, `Estructura_Red`, `Nro_Puertos`, `approval_Index`) VALUES
(1, 'ONU\r\n', 'ZXHNF660\r\n', 'ZTE\r\n', 200, 1, 2018, 0, 10, 7.0611),
(2, 'ROUTERBOARD\r\n', 'Hex-RB760IGS\r\n', 'MIKROTIK\r\n', 120, 1000, 2018, 0, 6, 8.48953),
(3, 'ONU\r\n', 'ZTE-F668\r\n', 'ZTE\r\n', 100, 500, 2015, 0, 3, 6.27206),
(4, 'ONU', 'ZTE-F660V6.0', 'ZTE', 120, 1, 2019, 0, 1, 7.21401),
(5, 'ROUTERBOARD', 'RB951G-2HnD', 'MIKROTIK', 100, 1000, 2019, 0, 5, 8.46096),
(6, 'ONU', 'ZTE-F643', 'ZTE', 20, 100, 2018, 0, 5, 5.71721),
(7, 'ONU', 'ZTE-F660', 'ZTE', 35, 1000, 2019, 0, 5, 6.37564),
(8, 'ONU', 'ZTE-F627', 'ZTE', 38, 1000, 2020, 0, 4, 6.35267),
(9, 'ONU', 'ZTE-F600', 'ZTE', 37, 100, 2000, 0, 5, 5.95173),
(10, 'ONU', 'HG8310M', 'ZTE', 40, 1000, 2010, 0, 4, 6.20857),
(11, 'OLT', 'ZXA10 C320', 'ZTE', 865, 10, 2015, 1, 10, 6.08402),
(12, 'OLT', 'MA5800-X17', 'HUAWEI', 980, 20, 2012, 1, 20, 7.25501),
(13, 'OLT', 'V1600G1-B', 'Vsol GPON', 740, 10, 2013, 1, 15, 6.03311),
(14, 'OLT', 'V1600GS-O32', 'Vsol EPON', 700, 5, 2018, 1, 20, 5.77318),
(15, 'OLT', 'P1201-08', 'TP-LINK', 930, 100, 2011, 1, 10, 7.66526),
(16, 'OLT', 'FD1608S-B0', 'C-DATA', 685, 1, 2009, 1, 10, 7.2617),
(17, 'ROUTERBOARD', 'RB3011UiAS', 'Mikrotik', 575, 10, 2010, 1, 11, 7.05393),
(18, 'ROUTERBOARD', 'CCR2004-1G-12S+2XS', 'Mikrotik', 455, 15, 2000, 1, 15, 5.87484),
(19, 'ROUTERBOARD', 'CCR1009-7G-1C-1S+', 'Mikrotik', 130, 20, 2005, 1, 20, 6.80691),
(20, 'ROUTERBOARD', 'RB951Ui-2HnD', 'Mikrotik', 230, 10, 2009, 1, 20, 8.05826),
(21, 'ROUTERBOARD\r\n', 'RB4011iGS+\r\n', 'Mikrotik', 160, 100, 2007, 1, 15, 5.50591),
(22, 'ROUTERBOARD', 'RB760iGS', 'Mikrotik', 267, 10, 2004, 2, 30, 8.74004),
(23, 'SWITCH', 'DGS-125', 'D-Link', 320, 50, 2006, 1, 50, 5.92609),
(24, 'SWITCH', 'FlexPoE', 'NETGEAR', 535, 20, 2017, 1, 30, 6.19261),
(25, 'SWITCH', 'ESS9300', 'Cisco', 206, 100, 2013, 2, 40, 8.19732),
(26, 'SWITCH', '10GbE', 'QNAP', 496, 1, 2000, 2, 40, 6.95331),
(27, 'SWITCH', 'SE3008', 'Linksys', 653, 5, 2001, 2, 50, 6.27974);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estructura`
--

CREATE TABLE `estructura` (
  `id` int(30) NOT NULL,
  `equipo` varchar(50) NOT NULL,
  `modelo` varchar(50) NOT NULL,
  `marca` varchar(50) NOT NULL,
  `caracteristica` varchar(60) NOT NULL,
  `costo` int(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `descripcion` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id_rol`, `descripcion`) VALUES
(1, 'administrador'),
(2, 'usuario');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `id_rol` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `correo`, `password`, `id_rol`) VALUES
(1, 'Frank Torres', 'frank@gmail.com', '123', 1),
(3, 'Liam', 'liam@gmail.com', '123', 2),
(10, 'paolo', 'paolo@gmail.com', '123', 2),
(12, 'sonia', 'sonia@gmail.com', '12345', 2),
(13, 'andre', 'andre@gmail.com', '123', 2),
(14, 'jefrin', 'jefrin@upn.pe', '123', 2);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `componentes`
--
ALTER TABLE `componentes`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `estructura`
--
ALTER TABLE `estructura`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_rol`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_rol` (`id_rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `componentes`
--
ALTER TABLE `componentes`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT de la tabla `estructura`
--
ALTER TABLE `estructura`
  MODIFY `id` int(30) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
