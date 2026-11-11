export const referralSignal = {
  id: "REF-001",
  urgency: "High",
  condition: "Obstetric emergency",
  originFacility: "Community Health Centre",
  requiredServices: [
    "Comprehensive obstetric care",
    "Caesarean section",
    "Blood transfusion",
  ],
  coordinates: [36.8219, -1.2921],
};

export const facilities = [
  {
    id: "pumwani",
    name: "Pumwani Maternity Hospital",
    level: 5,

    coordinates: [36.84552, -1.28028],

    facilityType: "Secondary care hospital",
    county: "Nairobi",
    subCounty: "Kamukunji",

    cemonc: true,
    bmonc: true,
    cSection: true,

    // KMHFR page does not explicitly list blood transfusion
    bloodTransfusion: false,

    maternityBeds: 0,
    maternityTheatres: 2,
    icuBeds: 0,
    hduBeds: 0,

    highRiskANC: true,
    focusedANC: true,

    open24Hours: true,
    operational: true,

    status: "Available",

    source: "KMHFR",
  },

  {
    id: "mama-lucy",
    name: "Mama Lucy Kibaki Hospital",
    level: 5,

    coordinates: [36.89843, -1.27416],

    facilityType: "Secondary care hospital",
    county: "Nairobi",
    subCounty: "Embakasi Central",

    cemonc: true,
    bmonc: true,
    cSection: true,
    bloodTransfusion: true,

    maternityBeds: 17,
    maternityTheatres: 3,
    icuBeds: 2,
    hduBeds: 2,

    highRiskANC: false,
    focusedANC: true,

    open24Hours: true,
    operational: true,

    status: "Available",

    source: "KMHFR",
  },

  {
    id: "knh",
    name: "Kenyatta National Hospital",
    level: 6,

    coordinates: [36.80734, -1.30088],

    facilityType:
      "Comprehensive Teaching & Tertiary Referral Hospital",

    county: "Nairobi",
    subCounty: "Kibra",

    cemonc: true,
    bmonc: true,
    cSection: true,
    bloodTransfusion: true,

    maternityBeds: 0,
    maternityTheatres: 0,
    icuBeds: 0,
    hduBeds: 0,

    highRiskANC: true,
    focusedANC: true,

    open24Hours: true,
    operational: true,

    status: "Available",

    source: "KMHFR",
  },
];