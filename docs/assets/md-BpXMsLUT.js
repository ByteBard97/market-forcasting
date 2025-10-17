import{b as d,o as u,w as l,g as e,e as s,a9 as t,v as c,x as _,T as r}from"./modules/vue-CDNPdEpt.js";import{_ as f,I as i,aA as n,au as y,av as h}from"./index-DHhrtO1V.js";import{I as g}from"./slidev/default-BvOGc6R3.js";import"./modules/unplugin-icons-BCEpU1sy.js";import"./modules/file-saver-B7oFTzqn.js";import"./modules/shiki-D1IkZTj0.js";const v={class:"slide-body"},x={__name:"HowToUseSlide",setup(p){return i(),(a,o)=>(u(),d(y,null,{default:l(()=>[o[4]||(o[4]=e("div",{class:"slide-header"},[e("h1",null,"How to Use Prophet for Your Business"),e("p",{class:"subtitle"},"Practical steps to start forecasting with your own data")],-1)),e("div",v,[s(n,{number:"1",title:"Gather Your Data"},{default:l(()=>[...o[0]||(o[0]=[e("p",null,"You need at minimum:",-1),e("ul",null,[e("li",null,[t("📅 "),e("strong",null,"Date"),t(" - Daily sales dates")]),e("li",null,[t("📊 "),e("strong",null,"Sales volume"),t(" - Pairs sold per day")]),e("li",null,[t("🎯 "),e("strong",null,"1+ year of history"),t(" - More is better")])],-1),e("div",{class:"example-box"},[e("strong",null,"Example CSV:"),e("pre",null,`date,pairs_sold
2023-01-01,45
2023-01-02,52
2023-01-03,48`)],-1)])]),_:1}),s(n,{number:"2",title:"Install Prophet"},{default:l(()=>[...o[1]||(o[1]=[e("p",null,"Two options:",-1),e("div",{class:"option"},[e("strong",null,"🐍 Python (recommended)"),e("pre",null,"pip install prophet pandas")],-1),e("div",{class:"option"},[e("strong",null,"📈 R"),e("pre",null,"install.packages('prophet')")],-1)])]),_:1}),s(n,{number:"3",title:"Run the Forecast"},{default:l(()=>[...o[2]||(o[2]=[e("pre",{class:"code-example"},`import pandas as pd
from prophet import Prophet

# Load your data
df = pd.read_csv('shoe_sales.csv')
df.columns = ['ds', 'y']  # Prophet needs these names

# Create and fit model
model = Prophet()
model.fit(df)

# Forecast next 90 days
future = model.make_future_dataframe(periods=90)
forecast = model.predict(future)

# Plot results
model.plot(forecast)`,-1)])]),_:1}),s(n,{number:"4",title:"Use the Forecast"},{default:l(()=>[...o[3]||(o[3]=[e("ul",null,[e("li",null,[t("📦 "),e("strong",null,"Order inventory"),t(" based on yhat (predicted demand)")]),e("li",null,[t("📊 "),e("strong",null,"Check uncertainty"),t(" - look at yhat_lower and yhat_upper")]),e("li",null,[t("🔄 "),e("strong",null,"Update weekly"),t(" - retrain as new data comes in")]),e("li",null,[t("⚠️ "),e("strong",null,"Trust but verify"),t(" - compare predictions to actual sales")])],-1),e("div",{class:"tip-box"},[t(" 💡 "),e("strong",null,"Pro tip:"),t(' Add your promotions and drops as "holidays" in Prophet for better accuracy ')],-1)])]),_:1})])]),_:1}))}},b=f(x,[["__scopeId","data-v-46080aad"]]),B={__name:"slides.md__slidev_18",setup(p){const{$clicksContext:a,$frontmatter:o}=i();return a.setup(),(P,w)=>{const m=b;return u(),d(g,c(_(r(h)(r(o),17))),{default:l(()=>[s(m)]),_:1},16)}}};export{B as default};
