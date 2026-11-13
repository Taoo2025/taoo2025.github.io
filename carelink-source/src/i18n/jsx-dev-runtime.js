export {Fragment} from './jsx-runtime';
import {jsx,jsxs} from './jsx-runtime';
export function jsxDEV(type,props,key,isStaticChildren){return (isStaticChildren?jsxs:jsx)(type,props,key)}
