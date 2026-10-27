import React,{useEffect,useState} from "react";
import {createRoot} from "react-dom/client";
import {ShieldCheck,ShieldAlert,Activity,BrainCircuit,Search,ArrowRight,Database,GitBranch,LockKeyhole,ExternalLink} from "lucide-react";
import "./style.css";

const API=(import.meta.env.VITE_API_URL || "http://127.0.0.1:8000").replace(/\/$/, "");
type Result=any;

function App(){
 const [url,setUrl]=useState(""); const [result,setResult]=useState<Result>(null);
 const [health,setHealth]=useState<any>({api:"checking",model_loaded:false}); const [busy,setBusy]=useState(false);
 useEffect(()=>{fetch(API+"/api/health").then(r=>r.json()).then(setHealth).catch(()=>setHealth({api:"offline",model_loaded:false}))},[]);
 async function analyze(){
  if(!url.trim())return; setBusy(true); setResult(null);
  try{let r=await fetch(API+"/api/analyze",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({url})});setResult(await r.json())}
  catch{setResult({status:"error",message:"FastAPI backend is offline. Start backend first."})}
  setBusy(false);
 }
 const ready=health.api==="online"&&health.model_loaded;
 return <div className="page">
  <nav><div className="logo"><div className="mark">PX</div><div><b>Phish<span>XAI</span></b><small>EXPLAINABLE URL INTELLIGENCE</small></div></div>
   <div className="navlinks"><a href="#analyze">Analyzer</a><a href="#workflow">Workflow</a><a href="#research">Research</a></div>
   <div className="live"><i className={health.api==="online"?"green":""}></i> API {health.api==="online"?"ONLINE":"OFFLINE"} <em>Â·</em> MODEL {ready?"READY":"NOT READY"}</div>
  </nav>
  <main>
   <section className="hero" id="analyze">
    <div className="tag"><ShieldCheck size={15}/> KUST BSCS Â· FINAL YEAR PROJECT</div>
    <h1>Detect phishing.<br/><span>Explain every decision.</span></h1>
    <p className="lead">A research-oriented platform that combines URL feature engineering, XGBoost classification, and SHAP explainability for transparent phishing detection.</p>
    <div className="scanner">
      <div className="inputrow"><Search size={20}/><input value={url} onChange={e=>setUrl(e.target.value)} onKeyDown={e=>e.key==="Enter"&&analyze()} placeholder="Paste a URL to analyze â€” e.g. https://example.com/login"/><button onClick={analyze} disabled={busy}>{busy?"ANALYZING":"ANALYZE URL"} <ArrowRight size={17}/></button></div>
      <div className="hint"><LockKeyhole size={13}/> Analysis is performed by the connected local API. No real model output is fabricated.</div>
    </div>
   </section>

   <section className="dashboard">
    <div className="panel prediction">
      <div className="panelhead"><div><span>01</span> PREDICTION</div><label className={ready?"ok":"warn"}>{ready?"MODEL CONNECTED":"MODEL NOT READY"}</label></div>
      {!result&&<div className="placeholder"><Activity size={30}/><b>Awaiting URL analysis</b><p>Enter a URL above to see a real model result.</p></div>}
      {result?.status==="model_not_ready"&&<div className="notready"><BrainCircuit size={35}/><h3>Model not connected</h3><p>{result.message}</p></div>}
      {result?.status==="error"&&<div className="notready"><ShieldAlert size={35}/><h3>Backend unavailable</h3><p>{result.message}</p></div>}
      {result?.status==="ok"&&<div className="predictionbody"><div className={"bigresult "+(result.prediction==="Phishing"?"danger":"safe")}>{result.prediction==="Phishing"?<ShieldAlert/>:<ShieldCheck/>}<strong>{result.prediction}</strong></div><div className="score"><span>CONFIDENCE</span><b>{(result.confidence*100).toFixed(2)}%</b><div><i style={{width:(result.confidence*100)+"%"}}/></div></div></div>}
    </div>
    <div className="panel">
      <div className="panelhead"><div><span>02</span> SHAP EXPLANATION</div><label>FEATURE IMPACT</label></div>

      {result?.status === "ok" && result.shap?.length ? (
        <div className="shaps">
          {result.shap.map((s: any) => (
            <div className="shap" key={s.feature}>
              <div>
                <b>{s.feature}</b>
                <span>
                  {s.impact >= 0 ? "+" : ""}
                  {s.impact.toFixed(4)}
                </span>
              </div>
              <div className="bar">
                <i
                  style={{
                    width:
                      Math.min(100, Math.abs(s.impact) * 100) + "%",
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="placeholder">
          <GitBranch size={30} />
          <b>Explainability layer</b>
          <p>
            SHAP feature contributions appear after a valid trained XGBoost
            model is connected.
          </p>
        </div>
      )}
    </div>
   </section>

   <section className="metrics">
    <div><Database/><b>URL FEATURES</b><span>Structural signals</span></div><div><BrainCircuit/><b>XGBOOST</b><span>Binary classification</span></div><div><GitBranch/><b>SHAP</b><span>Local explanations</span></div><div><LockKeyhole/><b>REAL-TIME API</b><span>FastAPI pipeline</span></div>
   </section>

   <section className="workflow" id="workflow">
    <div className="sectiontitle"><span>RESEARCH PIPELINE</span><h2>From URL to an explainable decision.</h2></div>
    <div className="steps"><article><small>01</small><h3>Input URL</h3><p>The user submits a URL through the responsive web interface.</p></article><article><small>02</small><h3>Feature Extraction</h3><p>URL structure is transformed into the same feature schema used by training.</p></article><article><small>03</small><h3>XGBoost</h3><p>The trained classifier produces a phishing or legitimate classification.</p></article><article><small>04</small><h3>SHAP</h3><p>Feature-level contributions provide an interpretable explanation.</p></article></div>
   </section>

   <section className="research" id="research">
    <div className="researchtext"><span>ABOUT PHISHXAI</span><h2>Cybersecurity research with transparency at the center.</h2><p>This platform is designed as a demonstration layer for an FYP research pipeline. It separates the interface, API, feature extraction, trained model, and explainability components so that every prediction can be traced to a real model output.</p></div>
    <div className="researchcard"><div><b>Model</b><span>XGBoost</span></div><div><b>Explainability</b><span>SHAP</span></div><div><b>Backend</b><span>FastAPI</span></div><div><b>Frontend</b><span>React + TypeScript</span></div></div>
   </section>
  </main>
  <footer><div><b>PhishXAI</b> Â· Explainable XGBoost-Based Phishing URL Detection</div><span>KUST Â· BS Computer Science Â· FYP Research Prototype</span></footer>
 </div>
}
createRoot(document.getElementById("root")!).render(<App/>);

