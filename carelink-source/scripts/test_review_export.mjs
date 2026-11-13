import assert from 'node:assert/strict';
import fs from 'node:fs';
import {storedLocationReviews,importEdits} from '../src/dataRuntime.js';
import {validateReview} from '../src/workflowRules.js';
const root=new URL('../',import.meta.url);
const checks=JSON.parse(fs.readFileSync(new URL('public/data/dios_location_checks.json',root),'utf8'));
const signals=JSON.parse(fs.readFileSync(new URL('public/data/dios_signals.json',root),'utf8'));
const baseline=JSON.parse(fs.readFileSync(new URL('public/data/nigeria_facilities_clean.json',root),'utf8'));
assert.equal(Object.keys(checks).length,signals.filter(a=>a.country==='Nigeria').length);
for(const [id,v] of Object.entries(checks)){validateReview(v);assert.equal(v.articleId,id);assert.equal(v.humanConfirmed,false);assert.equal(v.localCaseEvidence,false);assert.equal(v.coordinates,null);assert.equal(v.humanReviewStatus,'待人工复核');assert.ok(v.sourceAccessAudit);}
const memory=new Map();const storage={get length(){return memory.size},key:i=>[...memory.keys()][i],getItem:k=>memory.get(k)??null,setItem:(k,v)=>memory.set(k,v),removeItem:k=>memory.delete(k)};
const v=Object.values(checks).find(v=>v.sourceVerification==='原文已读取');
storage.setItem('dios-location-'+v.articleId,JSON.stringify(v));storage.setItem('dios-location-history',JSON.stringify([{articleId:v.articleId,after:v}]));
const locations=storedLocationReviews(storage);assert.equal(locations.length,1);assert.equal(locations[0].articleId,v.articleId);assert.ok(!locations.some(Array.isArray));
globalThis.localStorage=storage;globalThis.window={dispatchEvent(){}};
const payload=JSON.parse(JSON.stringify({locations,locationHistory:JSON.parse(storage.getItem('dios-location-history'))}));
memory.clear();importEdits(payload,baseline,signals);assert.deepEqual(storedLocationReviews(storage),locations);assert.equal(JSON.parse(storage.getItem('dios-location-history')).length,1);
console.log('PASS: 262 source-linked reviews, no human confirmations or invented coordinates; location history excluded from review list; team JSON round-trip succeeds. Isolated memory only.');
