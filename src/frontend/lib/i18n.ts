import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Import translation files
import en from '../locales/en/common.json';
import am from '../locales/am/common.json';
import om from '../locales/om/common.json';

const resources = {
  en: {
    common: en,
  },
  am: {
    common: am,
  },
  om: {
    common: om,
  },
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: 'en',
    debug: process.env.NODE_ENV === 'development',
    
    interpolation: {
      escapeValue: false,
    },
    
    detection: {
      order: ['localStorage', 'navigator', 'htmlTag'],
      caches: ['localStorage'],
    },
    
    ns: ['common'],
    defaultNS: 'common',
  });

export default i18n;
