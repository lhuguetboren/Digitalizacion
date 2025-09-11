<!doctype html>
<html lang="ca">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    :root{
      --bg:#f7f7fb; --card:#ffffff; --ink:#1f2330; --muted:#60657b; --ok:#0d7a5f; --bad:#ba1a1a; --brand:#3b5bfd; --line:#e6e7ee;
    }
    *{box-sizing:border-box}
    body{margin:0; font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,"Helvetica Neue",Arial,sans-serif; color:var(--ink); background:var(--bg);}
    .wrap{max-width:900px; margin:40px auto; padding:0 20px;}
    header{margin-bottom:20px}
    h1{font-size:1.6rem; margin:0 0 6px}
    p.lead{color:var(--muted); margin:0}
    form{background:var(--card); border:1px solid var(--line); border-radius:16px; padding:24px; box-shadow:0 1px 2px rgba(0,0,0,.04);}
    .meta{display:flex; gap:12px; margin-bottom:16px; flex-wrap:wrap}
    .meta input{padding:10px 12px; border:1px solid var(--line); border-radius:10px; outline:0; min-width:220px}
    .q{
      border-top:1px solid var(--line);
      padding-top:18px; margin-top:18px;
    }
    .q:first-of-type{border-top:0; padding-top:0; margin-top:0}
    .q h2{font-size:1rem; margin:0 0 10px}
    .options{display:grid; gap:10px; margin-top:8px}
    label.opt{
      display:flex; align-items:flex-start; gap:10px; padding:10px 12px; border:1px solid var(--line);
      border-radius:12px; cursor:pointer; transition:background .15s,border-color .15s;
      background:#fff;
    }
    label.opt:hover{border-color:#cfd2e3; background:#fafbff}
    .opt input{margin-top:2px}
    textarea{
      width:100%; min-height:120px; padding:12px; border:1px solid var(--line); border-radius:12px; resize:vertical;
      font:inherit;
    }
    .actions{display:flex; gap:12px; margin-top:22px; flex-wrap:wrap}
    button{
      appearance:none; border:0; padding:12px 16px; border-radius:12px; font-weight:600; cursor:pointer;
    }
    button[type="submit"]{background:var(--brand); color:white}
    button[type="reset"]{background:#eef0ff; color:#223}
    .result{
      display:none; margin:-8px 0 16px; padding:10px 12px; border-radius:10px; font-weight:600;
    }
    .result.ok{display:block; background:#e6f5ef; color:var(--ok); border:1px solid #bfe8d8}
    .result.bad{display:block; background:#fdeeee; color:var(--bad); border:1px solid #f6c9c9}
    .feedback{margin-top:8px; font-size:.95rem}
    .tag{display:inline-block; font-size:.8rem; padding:2px 8px; border-radius:999px; background:#eef0ff; color:#334; margin-left:8px}
    .correct{outline:2px solid var(--ok)}
    .incorrect{outline:2px solid var(--bad)}
    footer{margin-top:16px; color:var(--muted); font-size:.9rem}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <h1>Test RA1 <span class="tag">Digitalització, IT &amp; OT</span></h1>
      <p class="lead">Exemple de test</p>
    </header>

    <form id="quiz">


      <div id="result" class="result" aria-live="polite"></div>

      <!-- P1 -->
      <section class="q" data-q="1">
        <h2>1) Quina definició descriu millor la <em>digitalització</em> en una empresa?</h2>
        <div class="options">
          <label class="opt">
            <input type="radio" name="q1" value="A" required>
            <span>A) Escanejar documents i passar-los a PDF, sense canviar processos.</span>
          </label>
          <label class="opt">
            <input type="radio" name="q1" value="B">
            <span>B) Comprar equips informàtics nous sense modificar l’organització.</span>
          </label>
          <label class="opt">
            <input type="radio" name="q1" value="C" data-correct="true">
            <span>C) Convertir processos analògics en digitals i integrar tecnologies per crear valor i millorar l’eficiència.</span>
          </label>
          <label class="opt">
            <input type="radio" name="q1" value="D">
            <span>D) Substituir tot el personal per sistemes automàtics.</span>
          </label>
        </div>
      </section>

      <!-- P2 -->
      <section class="q" data-q="2">
        <h2>2) Quina opció descriu correctament la relació entre <strong>IT</strong> i <strong>OT</strong>?</h2>
        <div class="options">
          <label class="opt">
            <input type="radio" name="q2" value="A">
            <span>A) IT controla maquinària de planta i OT gestiona ERP i CRM.</span>
          </label>
          <label class="opt">
            <input type="radio" name="q2" value="B" data-correct="true">
            <span>B) IT gestiona informació i sistemes corporatius; OT supervisa i controla processos físics i actius industrials.</span>
          </label>
          <label class="opt">
            <input type="radio" name="q2" value="C">
            <span>C) IT i OT són el mateix; només canvia el nom segons el sector.</span>
          </label>
          <label class="opt">
            <input type="radio" name="q2" value="D">
            <span>D) OT només tracta de ciberseguretat; IT només de hardware.</span>
          </label>
        </div>
      </section>

      <!-- P3 -->
      <section class="q" data-q="3">
        <h2>3) Quin departament és típic d’un <em>entorn IT</em> dins d’una empresa?</h2>
        <div class="options">
          <label class="opt">
            <input type="radio" name="q3" value="A" data-correct="true">
            <span>A) Departament de TI / Sistemes d’Informació.</span>
          </label>
          <label class="opt">
            <input type="radio" name="q3" value="B">
            <span>B) Línia de producció i control de màquines CNC.</span>
          </label>
          <label class="opt">
            <input type="radio" name="q3" value="C">
            <span>C) Manteniment d’actius de planta (SCADA/PLC) exclusivament.</span>
          </label>
          <label class="opt">
            <input type="radio" name="q3" value="D">
            <span>D) Magatzem i picking.</span>
          </label>
        </div>
      </section>

      <!-- Oberta -->
      <section class="q" data-q="4">
        <h2>4) Pregunta oberta</h2>
        <p>Descriu <strong>un avantatge clau</strong> de connectar IT i OT en una empresa industrial i <strong>un risc associat</strong>. Proposa també <strong>una mesura de mitigació</strong>.</p>
        <textarea name="q4" placeholder="Resposta..." required></textarea>
      </section>

     

      <div class="feedback" id="fb"></div>

      
    </form>
  </div>

  <script>
    (function(){
      const form = document.getElementById('quiz');
      const result = document.getElementById('result');
      const fb = document.getElementById('fb');

      function clearMarks(){
        document.querySelectorAll('.opt').forEach(el=>{
          el.classList.remove('correct','incorrect');
        });
        result.className = 'result';
        result.style.display = 'none';
        result.textContent = '';
        fb.textContent = '';
      }

      form.addEventListener('reset', ()=>{
        setTimeout(clearMarks, 0);
      });

      form.addEventListener('submit', (e)=>{
        e.preventDefault();

        // Autocorrecció de les tancades (q1–q3)
        let total = 3, ok = 0;
        for (let i=1;i<=3;i++){
          const name = 'q'+i;
          const chosen = form.querySelector(`input[name="${name}"]:checked`);
          const options = form.querySelectorAll(`input[name="${name}"]`);
          options.forEach(inp=>{
            const label = inp.closest('label.opt');
            label.classList.remove('correct','incorrect');
          });
          if (chosen){
            const label = chosen.closest('label.opt');
            const isCorrect = !!chosen.dataset.correct;
            label.classList.add(isCorrect ? 'correct' : 'incorrect');
            if (isCorrect) ok++;
          }
        }

        // Missatge resultat
        const pct = Math.round((ok/total)*100);
        const good = ok === total;
        result.style.display = 'block';
        result.className = 'result ' + (good ? 'ok' : 'bad');
        result.textContent = `Encerts: ${ok}/${total} (${pct}%)`;

        // Feedback breu
        fb.innerHTML = `
          <ul>
            <li><strong>P1</strong>: la digitalització implica transformar processos i integrar tecnologia per crear valor.</li>
            <li><strong>P2</strong>: IT = informació i sistemes corporatius; OT = control de processos físics.</li>
            <li><strong>P3</strong>: el departament típic d’IT és TI/Sistemes d’Informació.</li>
            <li><strong>P4</strong> (oberta): s’avalua per criteri docent: claredat, fonamentació i proposta de mitigació.</li>
          </ul>
        `;

        // Scroll al resultat
        result.scrollIntoView({behavior:'smooth', block:'center'});
      });
    })();
  </script>
</body>
</html>
