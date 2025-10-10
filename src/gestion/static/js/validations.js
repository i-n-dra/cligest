async function run_validacion() {
  const run_input = document.getElementById("id_run_rep_legal");
  const help_text = document.getElementById("id_run_rep_legal_helptext");
  const run = run_input.value.trim();
  if (!run) return;

  const response = await fetch(`run-validacion/?run=${encodeURIComponent(run)}`);
  const data = await response.json();

  if (data.exists) {
    help_text.textContent = "Este RUN ya está registrado";
    help_text.style.color = "red";
  } else {
    help_text.textContent = "RUN disponible";
    help_text.style.color = "green";
  }
}