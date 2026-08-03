// ============================================================
// READER CITIES — the canonical readership geography, one source.
//
// Every entry is a real city from the PhilArchive readership log
// (Jun–Aug 2026). `tier` is the log's own readership band (3 = heaviest,
// 1 = lightest) and is the ONLY weight any surface may render from — no
// surface invents a position, a city, or a weight of its own.
//
// Consumed by:
//   · components/eip/HeroGlobe.astro — the hero globe's readership nodes
//   · pages/glass.astro              — the flat reach map
//
// The same 114 cities are mirrored in the two standalone static sites
// (OpenSesameAIEngineerPortfolio, ai-dev-resume-tldr-curator), which have
// no build step to import from. If this list changes, those change too.
//
// The headline counts quoted alongside these maps (countries, cities,
// downloads, institutions) are NOT derived from this array — they come
// from the readership log directly and are edited only against it. Do not
// recompute them by counting these entries.
// ============================================================

export interface ReaderCity {
  /** City name exactly as it appears in the readership log. */
  name: string;
  lat: number;
  lon: number;
  /** Readership band from the log: 3 heaviest, 1 lightest. */
  tier: 1 | 2 | 3;
}

export const READER_CITIES: ReaderCity[] = [
  { name: 'Ashburn', lat: 39, lon: -77.5, tier: 3 },
  { name: 'New York', lat: 40.7, lon: -74, tier: 3 },
  { name: 'Los Angeles', lat: 34, lon: -118.2, tier: 3 },
  { name: 'San Francisco', lat: 37.8, lon: -122.4, tier: 2 },
  { name: 'Chicago', lat: 41.9, lon: -87.6, tier: 3 },
  { name: 'Houston', lat: 29.8, lon: -95.4, tier: 3 },
  { name: 'Dallas', lat: 32.8, lon: -96.8, tier: 3 },
  { name: 'Phoenix', lat: 33.4, lon: -112.1, tier: 2 },
  { name: 'Seattle', lat: 47.6, lon: -122.3, tier: 2 },
  { name: 'Denver', lat: 39.7, lon: -105, tier: 2 },
  { name: 'Atlanta', lat: 33.7, lon: -84.4, tier: 2 },
  { name: 'Miami', lat: 25.8, lon: -80.2, tier: 2 },
  { name: 'Philadelphia', lat: 40, lon: -75.2, tier: 2 },
  { name: 'Washington', lat: 38.9, lon: -77, tier: 2 },
  { name: 'Nashville', lat: 36.2, lon: -86.8, tier: 1 },
  { name: 'Minneapolis', lat: 45, lon: -93.3, tier: 1 },
  { name: 'Montreal', lat: 45.5, lon: -73.6, tier: 3 },
  { name: 'Toronto', lat: 43.7, lon: -79.4, tier: 2 },
  { name: 'Ottawa', lat: 45.4, lon: -75.7, tier: 1 },
  { name: 'Vancouver', lat: 49.3, lon: -123.1, tier: 1 },
  { name: 'Mexico City', lat: 19.4, lon: -99.1, tier: 3 },
  { name: 'Tijuana', lat: 32.5, lon: -117, tier: 1 },
  { name: 'Querétaro', lat: 20.6, lon: -100.4, tier: 1 },
  { name: 'São Paulo', lat: -23.6, lon: -46.6, tier: 2 },
  { name: 'Rio de Janeiro', lat: -22.9, lon: -43.2, tier: 1 },
  { name: 'Belo Horizonte', lat: -19.9, lon: -43.9, tier: 1 },
  { name: 'Buenos Aires', lat: -34.6, lon: -58.4, tier: 2 },
  { name: 'Santiago', lat: -33.4, lon: -70.7, tier: 2 },
  { name: 'Bogotá', lat: 4.7, lon: -74.1, tier: 2 },
  { name: 'Medellín', lat: 6.2, lon: -75.6, tier: 1 },
  { name: 'Quito', lat: -0.2, lon: -78.5, tier: 1 },
  { name: 'La Paz', lat: -16.5, lon: -68.2, tier: 1 },
  { name: 'Montevideo', lat: -34.9, lon: -56.2, tier: 1 },
  { name: 'Ciudad del Este', lat: -25.5, lon: -54.6, tier: 1 },
  { name: 'Maracay', lat: 10.3, lon: -67.6, tier: 1 },
  { name: 'London', lat: 51.5, lon: -0.1, tier: 3 },
  { name: 'Paris', lat: 48.9, lon: 2.4, tier: 2 },
  { name: 'Berlin', lat: 52.5, lon: 13.4, tier: 1 },
  { name: 'Munich', lat: 48.1, lon: 11.6, tier: 2 },
  { name: 'Madrid', lat: 40.4, lon: -3.7, tier: 2 },
  { name: 'Rome', lat: 41.9, lon: 12.5, tier: 1 },
  { name: 'Bologna', lat: 44.5, lon: 11.3, tier: 1 },
  { name: 'Amsterdam', lat: 52.4, lon: 4.9, tier: 1 },
  { name: 'Brussels', lat: 50.9, lon: 4.4, tier: 1 },
  { name: 'Gothenburg', lat: 57.7, lon: 12, tier: 1 },
  { name: 'Lisbon', lat: 38.7, lon: -9.1, tier: 1 },
  { name: 'Dublin', lat: 53.3, lon: -6.3, tier: 1 },
  { name: 'Warsaw', lat: 52.2, lon: 21, tier: 1 },
  { name: 'Kyiv', lat: 50.5, lon: 30.5, tier: 2 },
  { name: 'Moscow', lat: 55.8, lon: 37.6, tier: 1 },
  { name: 'Sofia', lat: 42.7, lon: 23.3, tier: 1 },
  { name: 'Belgrade', lat: 44.8, lon: 20.5, tier: 1 },
  { name: 'Thessaloniki', lat: 40.6, lon: 22.9, tier: 1 },
  { name: 'Stuttgart', lat: 48.8, lon: 9.2, tier: 1 },
  { name: 'Chisinau', lat: 47, lon: 28.9, tier: 1 },
  { name: 'Casablanca', lat: 33.6, lon: -7.6, tier: 2 },
  { name: 'Rabat', lat: 34, lon: -6.8, tier: 1 },
  { name: 'Tunis', lat: 36.8, lon: 10.2, tier: 2 },
  { name: 'Cairo', lat: 30, lon: 31.2, tier: 1 },
  { name: 'Johannesburg', lat: -26.2, lon: 28, tier: 2 },
  { name: 'Nairobi', lat: -1.3, lon: 36.8, tier: 1 },
  { name: 'Accra', lat: 5.6, lon: -0.2, tier: 1 },
  { name: 'Dakar', lat: 14.7, lon: -17.5, tier: 1 },
  { name: 'Luanda', lat: -8.8, lon: 13.2, tier: 1 },
  { name: 'Addis Ababa', lat: 9, lon: 38.7, tier: 1 },
  { name: 'Dar es Salaam', lat: -6.8, lon: 39.2, tier: 1 },
  { name: 'Algiers', lat: 36.8, lon: 3.1, tier: 1 },
  { name: 'Tripoli', lat: 32.9, lon: 13.2, tier: 1 },
  { name: 'Bamako', lat: 12.6, lon: -8, tier: 1 },
  { name: 'Riyadh', lat: 24.7, lon: 46.7, tier: 3 },
  { name: 'Jeddah', lat: 21.5, lon: 39.2, tier: 2 },
  { name: 'Dubai', lat: 25.2, lon: 55.3, tier: 2 },
  { name: 'Doha', lat: 25.3, lon: 51.5, tier: 1 },
  { name: 'Baghdad', lat: 33.3, lon: 44.4, tier: 2 },
  { name: 'Erbil', lat: 36.2, lon: 44, tier: 2 },
  { name: 'Sulaymaniyah', lat: 35.6, lon: 45.4, tier: 1 },
  { name: 'Tel Aviv', lat: 32.1, lon: 34.8, tier: 1 },
  { name: 'Beirut', lat: 33.9, lon: 35.5, tier: 1 },
  { name: 'Amman', lat: 32, lon: 35.9, tier: 1 },
  { name: 'Manama', lat: 26.2, lon: 50.6, tier: 1 },
  { name: 'Kuwait City', lat: 29.4, lon: 48, tier: 1 },
  { name: 'Muscat', lat: 23.6, lon: 58.4, tier: 1 },
  { name: 'Istanbul', lat: 41, lon: 29, tier: 3 },
  { name: 'Ankara', lat: 39.9, lon: 32.9, tier: 1 },
  { name: 'Izmir', lat: 38.4, lon: 27.1, tier: 1 },
  { name: 'Beijing', lat: 39.9, lon: 116.4, tier: 3 },
  { name: 'Shanghai', lat: 31.2, lon: 121.5, tier: 2 },
  { name: 'Guangzhou', lat: 23.1, lon: 113.3, tier: 2 },
  { name: 'Chengdu', lat: 30.6, lon: 104.1, tier: 1 },
  { name: 'Hong Kong', lat: 22.3, lon: 114.2, tier: 2 },
  { name: 'Taipei', lat: 25, lon: 121.6, tier: 1 },
  { name: 'Singapore', lat: 1.35, lon: 103.8, tier: 3 },
  { name: 'Tokyo', lat: 35.7, lon: 139.7, tier: 1 },
  { name: 'Seoul', lat: 37.6, lon: 127, tier: 1 },
  { name: 'Hanoi', lat: 21, lon: 105.9, tier: 2 },
  { name: 'Ho Chi Minh City', lat: 10.8, lon: 106.6, tier: 2 },
  { name: 'Bangkok', lat: 13.8, lon: 100.5, tier: 1 },
  { name: 'Kuala Lumpur', lat: 3.1, lon: 101.7, tier: 2 },
  { name: 'Jakarta', lat: -6.2, lon: 106.8, tier: 2 },
  { name: 'Makati', lat: 14.6, lon: 121, tier: 2 },
  { name: 'Bandar Seri Begawan', lat: 4.9, lon: 114.9, tier: 1 },
  { name: 'Hyderabad', lat: 17.4, lon: 78.5, tier: 2 },
  { name: 'Mumbai', lat: 19.1, lon: 72.9, tier: 1 },
  { name: 'New Delhi', lat: 28.6, lon: 77.2, tier: 1 },
  { name: 'Lahore', lat: 31.6, lon: 74.3, tier: 2 },
  { name: 'Karachi', lat: 24.9, lon: 67, tier: 1 },
  { name: 'Islamabad', lat: 33.7, lon: 73.1, tier: 1 },
  { name: 'Dhaka', lat: 23.8, lon: 90.4, tier: 2 },
  { name: 'Tashkent', lat: 41.3, lon: 69.2, tier: 2 },
  { name: 'Almaty', lat: 43.2, lon: 76.9, tier: 1 },
  { name: 'Bishkek', lat: 42.9, lon: 74.6, tier: 1 },
  { name: 'Baku', lat: 40.4, lon: 49.9, tier: 1 },
  { name: 'Sydney', lat: -33.9, lon: 151.2, tier: 1 },
  { name: 'Melbourne', lat: -37.8, lon: 145, tier: 1 },
];

/** The log's leading city — the hub the globe's synapse threads radiate from. */
export const HUB_CITY = READER_CITIES[0];
