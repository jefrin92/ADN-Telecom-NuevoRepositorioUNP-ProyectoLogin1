-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 25-06-2024 a las 09:23:18
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `adn_telecom`
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
  `approval_Index` float NOT NULL,
  `descripcion` text NOT NULL,
  `Imagen` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `componentes`
--

INSERT INTO `componentes` (`ID`, `EQUIPO`, `MODELO`, `MARCA`, `COSTO`, `Velocidad_Red`, `Year`, `Estructura_Red`, `Nro_Puertos`, `approval_Index`, `descripcion`, `Imagen`) VALUES
(1, 'ONU', 'ZXHNF660', 'ZTE', 200, 1, 2018, 0, 10, 7.0611, 'ZTE ZXHN F660V6. 0 FTTH es una unidad terminal óptica GPON con puertos 1GE + 3FE + 2OLLAS + WIFI + 1USB Este modelo está diseñado para el escenario FTTH. Admite la función L3 para ayudar al suscriptor a construir una red doméstica inteligente.', 'https://th.bing.com/th/id/OIP.Pz4mXqbEYL9zS-cYyZk80AHaE8?rs=1&pid=ImgDetMain'),
(2, 'ONU', 'ZTE-F670L', 'ZTE', 150, 100, 2020, 0, 20, 8.48953, 'Admite Wi-Fi de transmisión múltiple de próxima generación, que opera simultáneamente en doble banda 802.11b/g/n@2.4G y 802.11a/n/ac@5G con una velocidad de hasta Gigabits y una excelente cobertura en interiores. Admite un enlace descendente de 2,488 Gbps y un enlace ascendente de 1,244 Gbps.', 'https://http2.mlstatic.com/D_NQ_NP_703457-MLA31353406875_072019-O.webp'),
(3, 'ONU', 'ZTE-F668', 'ZTE', 100, 500, 2015, 0, 3, 6.27206, 'Es un dispositivo rico en funciones que combina la tecnología GPON (red óptica pasiva Gigabit) y capacidades CATV (televisión por cable). Ofrece conectividad a Internet de alta velocidad y servicios de TV por cable en una sola unidad.', 'https://th.bing.com/th/id/OIP.F0D7ICcmz6u0U4i2alqjzQHaHa?rs=1&pid=ImgDetMain'),
(4, 'ONU', 'ZTE-F660V6.0', 'ZTE', 122, 1, 2019, 0, 1, 7.21401, 'ZTE ZXHN F660V6.0 FTTH es una unidad terminal óptica GPON con puertos 1GE + 3FE + 2OLLAS + WIFI + 1USB Este modelo está diseñado para el escenario FTTH. Admite la función L3 para ayudar al suscriptor a construir una red doméstica inteligente. Brinda a los suscriptores servicios convenientes, que incluyen voz, video (IPTV) y acceso a Internet de alta velocidad.', 'https://th.bing.com/th/id/OIP.X7FYsfkFmdP5hsbqJIsRwQAAAA?rs=1&pid=ImgDetMain'),
(5, 'ONU', 'ZTE-F660V5.2', 'ZTE', 22, 1000, 2021, 0, 4, 8.46096, 'Este modelo cumple con el estándar ITU-T G. 984, proporciona 2.488 enlace descendente de Gbps y 1.244 Enlace ascendente de Gbps en el lado de la red, y proporciona cuatro puertos GE, dos puertos POTS, uno 802.11b/g/n(2*2 @2.4GHz) interfaz wifi, una interfaz USB, y una interfaz RF en el lado del usuario.', 'https://s.alicdn.com/@sc04/kf/U5924c2cf05b64cb9a64670126f0de427N.jpg_720x720q50.jpg'),
(6, 'ONU', 'ZTE-F643', 'ZTE', 20, 100, 2018, 0, 5, 5.71721, 'Es un terminal de red óptica GPON diseñado para el escenario FTTH. Proporciona capacidades de reenvío de alto rendimiento para garantizar una excelente experiencia con Internet y servicios de video HD.. Tiene un pequeño, apariencia inteligente y verde, ventaja de ahorro de energía.', 'https://th.bing.com/th/id/OIP.9jqNniLD-c1cJT5D6O0gawHaHa?rs=1&pid=ImgDetMain'),
(7, 'ONU', 'ZTE-F660', 'ZTE', 35, 1000, 2019, 0, 5, 6.37564, 'Es un terminal de red óptica GPON diseñado para HGU (Unidad Home Gateway) utilizado en el escenario FTTH, que admite la función L3 para ayudar al suscriptor a construir una red doméstica inteligente. ZTE F660 proporciona una interfaz GPON para conectar OLT con una ODN.', 'https://th.bing.com/th/id/OIP.KTsT3tv5Sr2ldEywx11qzQHaHa?rs=1&pid=ImgDetMain'),
(8, 'ONU', 'ZTE-F627', 'ZTE', 38, 1000, 2020, 0, 4, 6.35267, 'ZTE GPON terminal ZXHN F627 FTTO or FTTH ONT With 4 FE+2POTS+WiFi, same function as F660 V5', 'https://th.bing.com/th/id/OIP.g-ai8Qmzfbz1gy30DqPftgHaHa?rs=1&pid=ImgDetMain'),
(9, 'ONU', 'ZTE-F600', 'ZTE', 37, 100, 2000, 0, 5, 5.95173, 'Proporciona soporte estable para IPTV y un acceso rápido a Internet, al mismo tiempo que es compacta y eficiente en energía. Al utilizar QoS en el F600, es posible brindar servicios que requieren una mayor capacidad de red para múltiples usuarios al mismo tiempo, permitiendo un funcionamiento sin problemas.', 'https://th.bing.com/th/id/OIP.fkZq0sp71cxtuOfxz4rrsgHaHa?rs=1&pid=ImgDetMain'),
(10, 'ONU', 'HG8310M', 'ZTE', 40, 1000, 2010, 0, 4, 6.20857, 'El Echo Life HG8310M es un terminal de red óptico interior (ONT) en la solución HUAWEI FTTH.Al utilizar la tecnología GPON, se proporciona acceso ultra ancha para usuarios domésticos y SOHO. El HG8310M proporciona un puerto Ethernet de GE.', 'https://th.bing.com/th/id/OIP.BwivpHBDhkgmKd4XQauJHQHaHa?rs=1&pid=ImgDetMain'),
(11, 'OLT', 'ZXA10 C320', 'ZTE', 865, 10, 2015, 1, 10, 6.08402, 'ZTE ZXA10 C320 es un terminal OLT en el conjunto con 2 controladores SMXA/1. La plataforma permite el uso de placas EPON, GPON y P2P, tiene 2 ranuras para tarjetas (altura de caja 2U).', 'https://americadigital.com.gt/wp-content/uploads/2022/02/EO145NZTEZXA10C320a.jpg'),
(12, 'OLT', 'MA5800-X17', 'HUAWEI', 980, 20, 2012, 1, 20, 7.25501, 'El chasis Huawei MA5800 X17 es un equipo modular para inserción de tarjetas, es una plataforma multiservicio diseñada para construir redes de acceso más amplias, rápidas e inteligentes, ofreciendo una mejor experiencia de servicio.', 'https://www.henanliyuan.com/Uploads/5d9176ab20d872779.jpg'),
(13, 'OLT', 'V1600G1-B', 'Vsol GPON', 740, 10, 2013, 1, 15, 6.03311, 'Los productos GPON OLT de la serie V1600G1-B son productos de montaje en bastidor de 19 pulgadas y 1U de altura. Las características de la OLT son pequeñas, convenientes, flexibles, fáciles de implementar y de alto rendimiento.', 'https://http2.mlstatic.com/D_NQ_NP_2X_730541-MLB44905216280_022021-F.jpg'),
(14, 'OLT', 'V1600GS-O32', 'Vsol EPON', 700, 5, 2018, 1, 20, 5.77318, ' Montaje en rack. Ancho de banda por puerto PON: Upstream 1.244Gbps, Downstream 2.488Gbps. Gestión amigable desede: EMS / Web / Telnet / CLI / Console.', 'https://cdn.myshoptet.com/usr/www.ponplanet.eu/user/shop/big/579_v1600gs-o32.jpg?65361b70'),
(15, 'OLT', 'P1201-08', 'TP-LINK', 930, 100, 2011, 1, 10, 7.66526, ' Es un producto de montaje en bastidor de 19 pulgadas de 1U, flexible y fácil de implementar, adecuado para diferentes escenarios de aplicación.', 'https://th.bing.com/th/id/OIP.R4_bV-hPjneL98gl34on7wAAAA?rs=1&pid=ImgDetMain'),
(16, 'OLT', 'FD1608S-B0', 'C-DATA', 685, 1, 2009, 1, 10, 7.2617, 'Es un dispositivo para montaje en rack de 1U con 1 interfaz USB, 4 puertos GE de enlace ascendente, 4 puertos SFP de enlace ascendente, 2*10GE de enlace ascendente y 8 puertos GPON. Cada puerto GPON admite una proporción de división de 1:128.', 'https://www.cyberteam.pl/_image/product/7746/7746_7746-fibertechnic-olt-gpon-fd1608s-b0-8xgpon-2x10gbit-4x1g-uplink-combo--2xac_03.jpg'),
(17, 'ROUTERBOARD', 'RB3011UiAS', 'Mikrotik', 575, 10, 2010, 1, 11, 7.05393, 'Presentamos el Router MikroTik RB3011UIAS-RM, la solución perfecta para sus necesidades de conectividad de red. Este router cuenta con un potente procesador de 1400MHz, 1GB de RAM, 10 puertos 10/100/1000 y 1 puerto SFP, convirtiéndolo en la solución ideal para cualquier red empresarial o doméstica.', 'https://www.comx-computers.co.za/i/mikrotik/52907_IMG1.jpg'),
(18, 'ROUTERBOARD', 'CCR2004-1G-12S+2XS', 'Mikrotik', 455, 15, 2000, 1, 15, 5.87484, 'Este potente router cuenta con un procesador de 4 núcleos, 4GB de RAM, 12 puertos SFP+ y 1 puerto Ethernet Gigabit. El CCR2004-1G-12S+2XS también incluye dos puertos SFP28 para ofrecerle la flexibilidad y velocidad que necesita para sacar el máximo partido a su red.', 'https://www.wisp.pl/galerie/m/mikrotik-cloud-core-router-cc_12697.jpg'),
(19, 'ROUTERBOARD', 'CCR1009-7G-1C-1S+', 'Mikrotik', 130, 20, 2005, 1, 20, 6.80691, 'El Router CCR1009-7G-1C-1S+ Mikrotik cuenta con puertos Ethernet totalmente independientes, cada uno con una conexión directa a la CPU, permitiendo superar la limitación compartida anterior de 1Gbit de los puertos switch-chip y utilizar todo el potencial de procesamiento de la CPU en esas puertas.', 'https://m.media-amazon.com/images/I/71Qp4cPJNIL._AC_SL1500_.jpg'),
(20, 'ROUTERBOARD', 'RB951Ui-2HnD', 'Mikrotik', 230, 10, 2009, 1, 20, 8.05826, 'RB951Ui-2HND RouterBOARD MikroTik 5p 10/100Mbps y 2.4GHz. Antena integrada de 2.5dBi, CPU de 1 núcleo de 600MHz, 128MB de RAM, potencia max. 30dBm, sistema operativo RouterOS y Licencia Nivel 4.', 'https://www.aibitech.com/3405-large_default/router-routerboard-mikrotik-rb951ui-2hnd-wireless-1000mw-24ghz-80211bgn-5-ethernet-1usb-l4.jpg'),
(21, 'ROUTERBOARD', 'RB4011iGS+', 'Mikrotik', 160, 100, 2007, 1, 15, 5.50591, 'El MikroTik RB4011iGS+RM es un dispositivo de múltiples puertos, ejecuta una CPU de arquitectura ARM para un rendimiento más alto. Cuenta con 10 puertos Gigabit LAN, 1 slot SFP+ 10Gbps (módulo no incluido), 1GB de memoria RAM.', 'https://i5.walmartimages.com/asr/c5ed70d8-aac4-4d60-8635-b631c8cf2a75.22c9c4934f589681eb65695ba5115cda.jpeg'),
(22, 'ROUTERBOARD', 'RB760iGS', 'Mikrotik', 267, 10, 2004, 2, 30, 8.74004, 'El RB760iGS hEX S es un dispositivo de enrutamiento versátil con una amplia gama de funciones de red, como firewall, VPN, balanceo de carga, control de ancho de banda, entre otros, está disponible para su uso. Sin duda el RB760iGS hEX S mejora su rendimiento y eficiencia de red.', 'https://http2.mlstatic.com/D_NQ_NP_2X_875988-MLA40175220158_122019-F.jpg'),
(23, 'SWITCH', 'DGS-125', 'D-Link', 320, 50, 2006, 1, 50, 5.92609, 'Incluye prevención ARP Spoofing, seguridad de puertos (hasta 64 direcciones MAC por puerto), IMP-Binding (IMPB) y D-Link Safeguard Engine.', 'https://www.media-rdc.com/medias/7f8c8641686c3c249d8455738091d3b3/switch-ethernet-dlink-dgs-105-dlink.jpg?cimgnr=CbzVv'),
(24, 'SWITCH', 'FlexPoE', 'NETGEAR', 535, 20, 2017, 1, 30, 6.19261, 'NETGEAR FlexPoE, disponible en determinados conmutadores NETGEAR PoE, le permite actualizar la potencia PoE del switch con nuevos adaptadores de alimentación sin sustituir todo el switch.', 'https://www.startechstore.com/wp-content/uploads/2020/09/NETGEAR-GS108LP-100EUS-121.jpg'),
(25, 'SWITCH', 'ESS9300', 'Cisco', 206, 100, 2013, 2, 40, 8.19732, 'La serie de conmutadores integrados Cisco Catalyst ESS9300 revoluciona la cartera de redes integradas de Cisco\r\ncon capacidades de alta velocidad y seguridad. El conmutador 10GE está optimizado para cumplir con el factor de forma especializado,\r\nla robustez, la densidad de puertos y las necesidades de energía de muchas aplicaciones que requieren personalización y complementa la gama estándar de conmutadores industriales de Cisco.\r\nla cartera de conmutación Ethernet industrial estándar de Cisco.\r\n\r\nTraducción realizada con la versión gratuita del traductor DeepL.com', 'https://th.bing.com/th/id/OIP.LUVQMn4D8uOxQJ7geOtK-QAAAA?rs=1&pid=ImgDetMain'),
(26, 'SWITCH', '10GbE', 'QNAP', 496, 1, 2000, 2, 40, 6.95331, '10GbE, abreviatura de 10 Gigabit Ethernet, se refiere a una red cableada ultrarrápida que transmite flujos de datos a una velocidad de 10 mil millones de bits por segundo.', 'https://th.bing.com/th/id/OIP.2mpkDZy8Dz2oMe27PFzjoAHaHa?rs=1&pid=ImgDetMain'),
(27, 'SWITCH', 'SE3008', 'Linksys', 653, 5, 2001, 2, 50, 6.27974, 'El Switch Linksys SE3008 Gigabit Ethernet de 8 puertos es un switch no administrado que ofrece una solución rápida y fácil para ampliar la red de su oficina con una instalación conecta y reproduce. También es útil para transferir datos a través de una red local hasta velocidades Gigabit.', 'https://th.bing.com/th/id/OIP.RUDBP-TbO7bUc1uNzelY4QHaHa?rs=1&pid=ImgDetMain');

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `descripcion` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `correo`, `password`, `id_rol`) VALUES
(1, 'Frank Torres', 'frank@gmail.com', '123', 1),
(10, 'paolo', 'paolo@gmail.com', '123', 2),
(12, 'sonia', 'sonia@gmail.com', '1234', 2),
(13, 'andre', 'andre@gmail.com', '123', 2),
(14, 'jefrin', 'jefrin@upn.pe', '123', 2),
(15, 'luis chira', 'luis@gmail.com', '123', 2),
(16, 'angela diaz', 'diaz@gmail.com', '123', 2),
(17, 'cristina morales', 'cristina@gmail.com', '123', 2),
(18, 'Test User', 'test_user@example.com', 'test_password', 2);

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
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
