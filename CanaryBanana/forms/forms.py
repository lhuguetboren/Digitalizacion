import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# El SCOPE requerido para crear y editar formularios
# Permite acceder y modificar el contenido y la configuración del formulario
SCOPES = ['https://www.googleapis.com/auth/forms.body'] 

def get_forms_service():
    """Autentica al usuario y devuelve el objeto de servicio de la API de Forms."""
    creds = None
    TOKEN_FILE = 'CanaryBanana/forms/token.json'  # Archivo donde se guardará el token de acceso

    # 1. Cargar las credenciales existentes si las hay
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # 2. Si no hay credenciales válidas, iniciar el flujo de autenticación
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Si el token expiró, usa el token de actualización
            creds.refresh(Request())
        else:
            # Inicia el flujo de la aplicación de escritorio
            # Usará tu archivo client_secret.json
            flow = InstalledAppFlow.from_client_secrets_file(
                '/CanaryBanana/forms/client_secret.json', SCOPES)
            
            # Esto abrirá una ventana del navegador para que inicies sesión
            creds = flow.run_local_server(port=0)

        # 3. Guardar las credenciales para la próxima ejecución
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    # 4. Crear y devolver el objeto de servicio de la API
    service = build('forms', 'v1', credentials=creds)
    return service

# Definición de un formulario simple en formato de diccionario Python (que se convierte a JSON)
# Paso 1: JSON solo para la CREACIÓN del formulario (solo info.title)
def create_initial_form_json(title: str):
    """Genera el diccionario JSON con solo el título para la creación inicial."""
    return {
        'info': {
            'title': title,
            'documentTitle': title,
        }
    }

# Paso 2: JSON para agregar ítems (preguntas) - ¡Índices corregidos!
def create_add_items_request(description: str):
    """Genera la lista de solicitudes (Requests) para agregar una descripción y preguntas."""
    
    requests = []

    # 1. ACTUALIZAR la descripción (Esto no requiere un índice de ubicación)
    requests.append({
        'updateFormInfo': {
            'info': {
                'description': description
            },
            'updateMask': 'description'
        }
    })

    # 2. Agregar la pregunta de Opción Múltiple (Primer elemento de pregunta: índice 0)
    requests.append({
        'createItem': {
            'item': {
                'title': 'Selecciona tu opción favorita:',
                'questionItem': {
                    'question': {
                        'required': True,
                        'choiceQuestion': {
                            'type': 'RADIO',
                            'options': [
                                {'value': 'Opción A'},
                                {'value': 'Opción B'},
                                {'value': 'Otra opción'}
                            ]
                        }
                    }
                }
            },
            'location': {
                'index': 0 # El PRIMER ítem de la lista va en el índice 0
            }
        }
    })

    # 3. Agregar la pregunta de Párrafo (Segundo elemento de pregunta: índice 1)
    requests.append({
        'createItem': {
            'item': {
                'title': '¿Algún comentario adicional?',
                'questionItem': {
                    'question': {
                        'required': False,
                        'textQuestion': {
                            'paragraph': True
                        }
                    }
                }
            },
            'location': {
                'index': 1 # El SEGUNDO ítem va en el índice 1
            }
        }
    })
    
    return {'requests': requests}

def create_and_update_form():
    """Crea y luego actualiza el formulario para añadir preguntas y descripción."""
    
    forms_service = get_forms_service()
    
    TITLE = "Formulario de Prueba Automatizado"
    DESCRIPTION = "Este formulario fue creado usando la Google Forms API con Python."
    
    # --- PASO 1: CREAR el formulario (solo título) ---
    initial_form_content = create_initial_form_json(TITLE)
    
    print(f"1/2. Creando formulario inicial '{TITLE}'...")
    try:
        # Crea el formulario y obtiene el objeto de respuesta, que incluye el 'formId'
        created_form = forms_service.forms().create(body=initial_form_content).execute()
        form_id = created_form['formId']
        print(f"   ✅ Formulario creado. ID: {form_id}")

    except Exception as e:
        print(f"   ❌ ERROR en la creación inicial: {e}")
        return

    # --- PASO 2: ACTUALIZAR el formulario (añadir preguntas y descripción) ---
    update_request_body = create_add_items_request(DESCRIPTION)
    
    print("2/2. Añadiendo preguntas y descripción...")
    try:
        # Usa batchUpdate con el formId para añadir los elementos.
        updated_form = forms_service.forms().batchUpdate(
            formId=form_id,
            body=update_request_body
        ).execute()

        print("   ✅ Formulario actualizado exitosamente!")
        print(f"   Enlace para responder: {created_form['responderUri']}")
        print(f"   Revisión del formulario: {updated_form['writeControl']['requiredRevisionId']}")

    except Exception as e:
        print(f"   ❌ ERROR en la actualización (batchUpdate): {e}")

# Ejecutar el flujo de creación y actualización
create_and_update_form()