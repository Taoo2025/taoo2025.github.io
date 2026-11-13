import {useContext} from 'react';
import {jsx as originalJsx,jsxs as originalJsxs,Fragment} from 'react/jsx-runtime';
import {LanguageContext} from './Language';
import {translate,chinese} from './translate';
export {Fragment};
function LocalizedElement({tag,original}){
 const language=useContext(LanguageContext);
 const props={...original};
 // Keep form values, event handlers, saved records and source data canonical.
 if(tag==='option'&&props.value===undefined&&typeof props.children==='string')props.value=props.children;
 {
  const convert=language==='en'?translate:chinese;
  const text=v=>typeof v==='string'?convert(v):Array.isArray(v)?v.map(text):v;
  if(tag!=='textarea'&&tag!=='script'&&tag!=='style')props.children=text(props.children);
  for(const key of ['placeholder','title','aria-label','alt'])if(typeof props[key]==='string')props[key]=convert(props[key]);
 }
 return (Array.isArray(props.children)?originalJsxs:originalJsx)(tag,props);
}
export function jsx(type,props,key){return typeof type==='string'?originalJsx(LocalizedElement,{tag:type,original:props},key):originalJsx(type,props,key)}
export function jsxs(type,props,key){return typeof type==='string'?originalJsxs(LocalizedElement,{tag:type,original:props},key):originalJsxs(type,props,key)}
