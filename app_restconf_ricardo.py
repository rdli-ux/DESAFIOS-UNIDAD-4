"""
Desarrollado por: Ricardo Daniel Lazo Ibarra
Práctica: RESTCONF con Python y Tkinter - Cisco DevNet Sandbox
Dispositivo Catalyst 8000v (IP: 10.10.20.48)[cite: 16]
"""

import json
import tkinter as tk
from tkinter import messagebox, ttk
import requests

# Deshabilitar advertencias de certificados SSL autofirmados
requests.packages.urllib3.disable_warnings()

# --- DATOS DE TU SANDBOX DE DEVNET ---
BASE_URL = "https://10.10.20.48/restconf/data/ietf-interfaces:interfaces"
AUTH = ("developer", "C1sco12345")
HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-type": "application/yang-data+json",
}


class RestconfSandboxApp:

  def __init__(self, root):
    self.root = root
    self.root.title("RESTCONF Sandbox - Ricardo Daniel")
    self.root.geometry("680x680")

    # --- TÍTULO PRINCIPAL ---
    title_label = tk.Label(
        root,
        text="Gestor RESTCONF - Catalyst 8000v (Ricardo Daniel)",
        font=("Arial", 13, "bold"),
        fg="#0277BD",
    )
    title_label.pack(pady=10)

    # --- FRAME DE ENTRADA DE DATOS (Formulario) ---
    form_frame = tk.LabelFrame(
        root,
        text=" Parámetros de la Interfaz (Sandbox DevNet) ",
        font=("Arial", 10, "bold"),
    )
    form_frame.pack(fill="x", padx=15, pady=5)

    # Nombre Interfaz
    tk.Label(form_frame, text="Nombre (ej. Loopback25):").grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )
    self.entry_name = tk.Entry(form_frame, width=28)
    self.entry_name.grid(row=0, column=1, padx=5, pady=5)
    self.entry_name.insert(0, "Loopback25")

    # Dirección IP
    tk.Label(form_frame, text="Dirección IP:").grid(
        row=1, column=0, sticky="w", padx=5, pady=5
    )
    self.entry_ip = tk.Entry(form_frame, width=28)
    self.entry_ip.grid(row=1, column=1, padx=5, pady=5)
    self.entry_ip.insert(0, "192.168.25.1")

    # Máscara
    tk.Label(form_frame, text="Máscara de Red:").grid(
        row=2, column=0, sticky="w", padx=5, pady=5
    )
    self.entry_mask = tk.Entry(form_frame, width=28)
    self.entry_mask.grid(row=2, column=1, padx=5, pady=5)
    self.entry_mask.insert(0, "255.255.255.0")

    # Descripción (Tu nombre para demostrar autoría)
    tk.Label(form_frame, text="Descripción:").grid(
        row=3, column=0, sticky="w", padx=5, pady=5
    )
    self.entry_desc = tk.Entry(form_frame, width=28)
    self.entry_desc.grid(row=3, column=1, padx=5, pady=5)
    self.entry_desc.insert(0, "Interfaz creada por Ricardo Daniel")

    # --- FRAME DE BOTONES DE ACCIÓN ---
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=12)

    self.btn_get = tk.Button(
        btn_frame,
        text="Consultar (GET)",
        bg="#2196F3",
        fg="white",
        font=("Arial", 9, "bold"),
        width=16,
        command=self.action_get,
    )
    self.btn_get.grid(row=0, column=0, padx=6)

    self.btn_put = tk.Button(
        btn_frame,
        text="Crear/Modificar (PUT)",
        bg="#4CAF50",
        fg="white",
        font=("Arial", 9, "bold"),
        width=18,
        command=self.action_put,
    )
    self.btn_put.grid(row=0, column=1, padx=6)

    self.btn_del = tk.Button(
        btn_frame,
        text="Eliminar (DELETE)",
        bg="#F44336",
        fg="white",
        font=("Arial", 9, "bold"),
        width=16,
        command=self.action_delete,
    )
    self.btn_del.grid(row=0, column=2, padx=6)

    # --- ÁREA DE TEXTO / RESPUESTA ---
    result_frame = tk.LabelFrame(
        root, text=" Respuesta del Servidor RESTCONF ", font=("Arial", 10, "bold")
    )
    result_frame.pack(fill="both", expand=True, padx=15, pady=5)

    self.text_output = tk.Text(result_frame, wrap="word", height=12)
    self.text_output.pack(fill="both", expand=True, padx=5, pady=5)

    # --- BARRA DE ESTADO INFERIOR (Indicador Visual UX) ---
    self.status_bar = tk.Label(
        root,
        text="Conectado al Sandbox: 10.10.20.48 (Ricardo Daniel)[cite: 16]",
        bd=1,
        relief=tk.SUNKEN,
        anchor="w",
        bg="#e0e0e0",
        fg="black",
        font=("Arial", 9),
    )
    self.status_bar.pack(side=tk.BOTTOM, fill="x")

  def update_status(self, text, success=True):
    """Cambia el color de la barra de estado según el resultado (Verde/Rojo)"""
    color = "#4CAF50" if success else "#F44336"
    self.status_bar.config(text=text, bg=color, fg="white")

  def action_get(self):
    """Realiza la petición GET para consultar la interfaz o el contenedor general"""
    if_name = self.entry_name.get().strip()
    url = f"{BASE_URL}/interface={if_name}" if if_name else BASE_URL

    try:
      resp = requests.get(url, auth=AUTH, headers=HEADERS, verify=False)
      if resp.status_code == 200:
        data = resp.json()
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert(tk.END, json.dumps(data, indent=4))
        self.update_status(
            f"STATUS 200 OK: Consulta exitosa de '{if_name}' (Ricardo Daniel).",
            True,
        )
      else:
        self.update_status(
            f"Error HTTP {resp.status_code}: Recurso no encontrado.", False
        )
        messagebox.showerror(
            "Error", f"Código de estado: {resp.status_code}\n{resp.text}"
        )
    except Exception as e:
      self.update_status("Error crítico de conexión VPN/Red.", False)
      messagebox.showerror("Excepción de Red", str(e))

  def action_put(self):
    """Crea o actualiza la interfaz usando PUT y enviando el diccionario YANG"""
    if_name = self.entry_name.get().strip()
    if_ip = self.entry_ip.get().strip()
    if_mask = self.entry_mask.get().strip()
    if_desc = self.entry_desc.get().strip()

    if not if_name:
      messagebox.showwarning("Advertencia", "El nombre de la interfaz es requerido.")
      return

    url = f"{BASE_URL}/interface={if_name}"
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": if_name,
            "description": if_desc,
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [{"ip": if_ip, "netmask": if_mask}]
            },
            "ietf-ip:ipv6": {},
        }
    }

    try:
      resp = requests.put(
          url,
          data=json.dumps(yangConfig),
          auth=AUTH,
          headers=HEADERS,
          verify=False,
      )
      if 200 <= resp.status_code <= 201:
        self.update_status(
            f"STATUS {resp.status_code}: Interfaz '{if_name}' creada con éxito"
            " por Ricardo Daniel.",
            True,
        )
        messagebox.showinfo(
            "Éxito",
            f"Interfaz configurada correctamente.\nCódigo HTTP:"
            f" {resp.status_code} (Created/OK)",
        )
      else:
        self.update_status(
            f"Error HTTP {resp.status_code} al enviar datos.", False
        )
        messagebox.showerror(
            "Error de API", f"Código: {resp.status_code}\n{resp.text}"
        )
    except Exception as e:
      self.update_status("Error de red al ejecutar PUT.", False)
      messagebox.showerror("Excepción", str(e))

  def action_delete(self):
    """Elimina la interfaz seleccionada pidiendo confirmación visual previa"""
    if_name = self.entry_name.get().strip()
    if not if_name:
      messagebox.showwarning(
          "Advertencia", "Ingresa el nombre de la interfaz a eliminar."
      )
      return

    confirm = messagebox.askyesno(
        "Confirmar Eliminación",
        f"¿Estás seguro de eliminar la interfaz '{if_name}' del Sandbox?",
    )
    if not confirm:
      return

    url = f"{BASE_URL}/interface={if_name}"

    try:
      resp = requests.delete(url, auth=AUTH, headers=HEADERS, verify=False)
      if 200 <= resp.status_code < 300:
        self.update_status(
            f"STATUS {resp.status_code}: Interfaz '{if_name}' eliminada por"
            " Ricardo Daniel.",
            True,
        )
        messagebox.showinfo(
            "Eliminado", f"La interfaz {if_name} ha sido borrada del router."
        )
        self.text_output.delete("1.0", tk.END)
      else:
        self.update_status(
            f"Error HTTP {resp.status_code} al intentar eliminar.", False
        )
        messagebox.showerror(
            "Error", f"No se pudo eliminar. Código: {resp.status_code}"
        )
    except Exception as e:
      self.update_status("Error de red en DELETE.", False)
      messagebox.showerror("Excepción", str(e))


if __name__ == "__main__":
  root = tk.Tk()
  app = RestconfSandboxApp(root)
  root.mainloop()