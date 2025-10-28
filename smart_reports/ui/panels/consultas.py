"""
Panel de Consultas de Usuarios
Búsqueda y visualización de usuarios con tksheet
"""
import customtkinter as ctk
from tkinter import messagebox
from smart_reports.config.identity import get_hutchison_theme, get_font
from smart_reports.ui.components.widgets import (
    AngledHeaderFrame,
    AngledCard,
    HutchisonLabel,
    HutchisonButton
)


class ConsultasPanel:
    """Panel de consultas y búsqueda de usuarios"""

    def __init__(self, parent, theme, conn=None, cursor=None):
        """
        Args:
            parent: Widget padre del panel
            theme: Tema corporativo Hutchison
            conn: Conexión a base de datos
            cursor: Cursor de base de datos
        """
        self.parent = parent
        self.theme = theme
        self.conn = conn
        self.cursor = cursor
        self.search_entry = None
        self.search_result_frame = None
        self.table_container = None
        self.users_sheet = None

    def show(self):
        """Mostrar panel de consultas"""
        # Header angulado
        header = AngledHeaderFrame(
            self.parent,
            text='Consultas de Usuarios',
            height=80,
            color=self.theme['secondary']
        )
        header.pack(fill='x', pady=(0, 20))

        if not self.conn:
            # Sin conexión a BD
            no_db_label = HutchisonLabel(
                self.parent,
                text='⚠️  No hay conexión a la base de datos\n\n' +
                     'Este panel requiere conexión activa para consultar usuarios.',
                label_type='body'
            )
            no_db_label.pack(pady=50)
            return

        # Card de búsqueda
        search_card = AngledCard(
            self.parent,
            title='Búsqueda de Usuarios',
            header_color=self.theme['primary']
        )
        search_card.pack(fill='x', pady=20)

        # Búsqueda por ID
        search_frame = ctk.CTkFrame(search_card.content_frame, fg_color='transparent')
        search_frame.pack(fill='x', pady=10)

        HutchisonLabel(
            search_frame,
            text='🔍  Buscar por User ID:',
            label_type='heading'
        ).pack(side='left', padx=(0, 15))

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text='Ingrese ID de usuario...',
            font=get_font('body', 14),
            width=300,
            height=40
        )
        self.search_entry.pack(side='left', padx=5)

        HutchisonButton(
            search_frame,
            text='Buscar',
            button_type='primary',
            width=120,
            command=self.search_user
        ).pack(side='left', padx=10)

        # Resultado de búsqueda
        self.search_result_frame = ctk.CTkFrame(
            search_card.content_frame,
            fg_color=self.theme['surface'],
            corner_radius=10
        )
        self.search_result_frame.pack(fill='both', expand=True, pady=(20, 0))

        search_result_label = HutchisonLabel(
            self.search_result_frame,
            text='Ingrese un User ID y haga clic en Buscar',
            label_type='body'
        )
        search_result_label.pack(pady=30)

        # Card de tabla de usuarios (con tksheet)
        table_card = AngledCard(
            self.parent,
            title='Todos los Usuarios (Tabla Interactiva)',
            header_color=self.theme['secondary']
        )
        table_card.pack(fill='both', expand=True, pady=20)

        # Botón para cargar tabla
        load_btn_frame = ctk.CTkFrame(table_card.content_frame, fg_color='transparent')
        load_btn_frame.pack(fill='x', pady=(10, 20))

        HutchisonButton(
            load_btn_frame,
            text='Cargar Todos los Usuarios',
            button_type='secondary',
            command=self.load_users_table
        ).pack(pady=10)

        # Container para la tabla
        self.table_container = ctk.CTkFrame(
            table_card.content_frame,
            fg_color=self.theme['background'],
            corner_radius=10,
            height=400
        )
        self.table_container.pack(fill='both', expand=True, padx=10, pady=10)
        self.table_container.pack_propagate(False)

    def search_user(self):
        """Buscar usuario por ID"""
        user_id = self.search_entry.get().strip()

        if not user_id:
            messagebox.showwarning("Advertencia", "Ingrese un User ID")
            return

        if not self.conn:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        try:
            self.cursor.execute("""
                SELECT u.UserId, u.Nombre, u.Email, un.NombreUnidad
                FROM Instituto_Usuario u
                LEFT JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
                WHERE u.UserId = ?
            """, (user_id,))

            result = self.cursor.fetchone()

            # Limpiar resultado anterior
            for widget in self.search_result_frame.winfo_children():
                widget.destroy()

            if result:
                # Mostrar resultado
                result_container = ctk.CTkFrame(self.search_result_frame, fg_color='transparent')
                result_container.pack(fill='both', expand=True, padx=30, pady=20)

                success_label = HutchisonLabel(
                    result_container,
                    text='✓ Usuario Encontrado',
                    label_type='heading'
                )
                success_label.configure(text_color=self.theme['secondary'])
                success_label.pack(pady=(0, 20))

                info_text = f"""User ID: {result[0]}
Nombre: {result[1] or 'N/A'}
Email: {result[2] or 'N/A'}
Unidad: {result[3] or 'N/A'}"""

                info_label = HutchisonLabel(
                    result_container,
                    text=info_text,
                    label_type='body'
                )
                info_label.configure(justify='left')
                info_label.pack()
            else:
                error_label = HutchisonLabel(
                    self.search_result_frame,
                    text=f'✗ No se encontró el usuario: {user_id}',
                    label_type='heading'
                )
                error_label.configure(text_color='#ff6b6b')
                error_label.pack(pady=30)

        except Exception as e:
            messagebox.showerror("Error", f"Error en búsqueda:\n{str(e)}")

    def load_users_table(self):
        """Cargar tabla de usuarios con tksheet"""
        if not self.conn:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        try:
            from tksheet import Sheet

            # Limpiar container
            for widget in self.table_container.winfo_children():
                widget.destroy()

            # Obtener datos de usuarios
            self.cursor.execute("""
                SELECT u.UserId, u.Nombre, u.Email, un.NombreUnidad
                FROM Instituto_Usuario u
                LEFT JOIN Instituto_UnidadDeNegocio un
                    ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
                ORDER BY u.UserId
            """)

            rows = self.cursor.fetchall()

            # Crear Sheet
            self.users_sheet = Sheet(
                self.table_container,
                data=[[row[0], row[1] or '', row[2] or '', row[3] or ''] for row in rows],
                headers=['User ID', 'Nombre', 'Email', 'Unidad de Negocio'],
                theme='light blue',
                height=380,
                width=900
            )

            # Personalizar colores
            self.users_sheet.set_options(
                header_bg=self.theme['secondary'],
                header_fg=self.theme['text_on_primary'],
                index_bg=self.theme['surface'],
                index_fg=self.theme['text'],
                table_bg=self.theme['background'],
                table_fg=self.theme['text'],
                table_selected_cells_bg=self.theme['primary'],
                table_selected_cells_fg=self.theme['text_on_primary']
            )

            # Habilitar funcionalidades
            self.users_sheet.enable_bindings(
                'single_select', 'row_select', 'column_width_resize',
                'arrowkeys', 'right_click_popup_menu', 'rc_select',
                'copy', 'select_all'
            )

            # Menú contextual
            self.users_sheet.popup_menu_add_command(
                'Eliminar fila seleccionada',
                self.delete_selected_row
            )

            self.users_sheet.pack(fill='both', expand=True)

            messagebox.showinfo(
                "Éxito",
                f"Se cargaron {len(rows)} usuarios en la tabla.\n\n" +
                "Funcionalidades disponibles:\n" +
                "• Click derecho para menú contextual\n" +
                "• Seleccionar filas\n" +
                "• Copiar datos (Ctrl+C)\n" +
                "• Redimensionar columnas"
            )

        except ImportError:
            error_label = HutchisonLabel(
                self.table_container,
                text='La librería tksheet no está instalada.\n\nInstálala con:\npip install tksheet',
                label_type='body'
            )
            error_label.configure(text_color='red')
            error_label.pack(expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar tabla:\n{str(e)}")

    def delete_selected_row(self):
        """Eliminar fila seleccionada de la tabla"""
        if not hasattr(self, 'users_sheet') or not self.users_sheet:
            return

        selected = self.users_sheet.get_currently_selected()

        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una fila primero")
            return

        row = selected.row if hasattr(selected, 'row') else selected[0]

        confirm = messagebox.askyesno(
            "Confirmar",
            "¿Desea eliminar la fila seleccionada de la tabla?\n\n" +
            "(Esto solo la quita de la vista, no de la base de datos)"
        )

        if confirm:
            self.users_sheet.delete_row(row)
            messagebox.showinfo("Éxito", "Fila eliminada de la tabla")
