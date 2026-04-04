"use client";

import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Globe, ChevronDown } from 'lucide-react';

const languages = [
  {
    code: 'en',
    name: 'English',
    flag: '🇺🇸',
    dir: 'ltr'
  },
  {
    code: 'am',
    name: 'አማርኛ',
    flag: '🇪🇹',
    dir: 'rtl'
  },
  {
    code: 'om',
    name: 'Afaan Oromoo',
    flag: '🇪🇹',
    dir: 'ltr'
  }
];

export default function LanguageSwitcher() {
  const { i18n } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);

  const currentLanguage = languages.find(lang => lang.code === i18n.language) || languages[0];

  const changeLanguage = (langCode: string, dir: string) => {
    i18n.changeLanguage(langCode);
    document.documentElement.dir = dir;
    document.documentElement.lang = langCode;
    localStorage.setItem('language', langCode);
    setIsOpen(false);
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 rounded-lg bg-surface-card border border-surface-border hover:bg-surface-hover transition-colors"
      >
        <Globe className="w-4 h-4 text-slate-400" />
        <span className="text-sm font-medium text-white">{currentLanguage.flag}</span>
        <span className="text-sm text-slate-300">{currentLanguage.name}</span>
        <ChevronDown className={`w-4 h-4 text-slate-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute top-full left-0 mt-2 w-56 bg-surface-card border border-surface-border rounded-lg shadow-lg z-50">
          <div className="p-1">
            {languages.map((language) => (
              <button
                key={language.code}
                onClick={() => changeLanguage(language.code, language.dir)}
                className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  i18n.language === language.code
                    ? 'bg-brand-600/20 text-brand-300 border border-brand-500/30'
                    : 'text-slate-400 hover:bg-surface-hover hover:text-white'
                }`}
              >
                <span className="text-lg">{language.flag}</span>
                <span>{language.name}</span>
                {i18n.language === language.code && (
                  <div className="ml-auto w-2 h-2 bg-brand-500 rounded-full"></div>
                )}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
