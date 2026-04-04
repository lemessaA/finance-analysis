"use client";

import "@/lib/i18n";
import { createContext, useContext, useEffect, ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

interface I18nContextType {
  language: string;
  changeLanguage: (lang: string) => void;
  t: (key: string) => string;
}

const I18nContext = createContext<I18nContextType | undefined>(undefined);

export function I18nProvider({ children }: { children: ReactNode }) {
  const { i18n, t } = useTranslation();

  useEffect(() => {
    const savedLanguage = localStorage.getItem('language') || 'en';
    if (savedLanguage !== i18n.language) {
      i18n.changeLanguage(savedLanguage);
    }
  }, [i18n]);

  const changeLanguage = (lang: string) => {
    i18n.changeLanguage(lang);
    localStorage.setItem('language', lang);
    
    // Update document direction for RTL languages
    const languages = {
      en: 'ltr',
      am: 'rtl',
      om: 'ltr'
    };
    
    document.documentElement.dir = languages[lang as keyof typeof languages] || 'ltr';
    document.documentElement.lang = lang;
  };

  return (
    <I18nContext.Provider value={{ language: i18n.language, changeLanguage, t }}>
      {children}
    </I18nContext.Provider>
  );
}

export function useI18n() {
  const context = useContext(I18nContext);
  if (context === undefined) {
    throw new Error('useI18n must be used within an I18nProvider');
  }
  return context;
}
