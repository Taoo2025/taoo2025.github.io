import {createContext,useState,useEffect} from 'react';
// Vite may prebundle the JSX adapter separately; share one context across both module graphs.
const contextKey=Symbol.for('carelink.language.context');
export const LanguageContext=globalThis[contextKey]||(globalThis[contextKey]=createContext('en'));
export function LanguageProvider({children}){
 const [language,setLanguage]=useState(()=>{try{return localStorage.getItem('carelink-language')==='cn'?'cn':'en'}catch{return 'en'}});
 useEffect(()=>{document.documentElement.lang=language==='en'?'en':'zh-CN';try{localStorage.setItem('carelink-language',language)}catch{}},[language]);
 return <LanguageContext.Provider value={language}><nav className="language-switch" aria-label="Language / 语言">{['cn','en'].map(l=><button key={l} type="button" lang={l==='cn'?'zh-CN':'en'} aria-pressed={language===l} onClick={()=>setLanguage(l)}>{l.toUpperCase()}</button>)}</nav>{children}</LanguageContext.Provider>;
}
