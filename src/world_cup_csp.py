import copy


class WorldCupCSP:
    def __init__(self, teams, groups, debug=False):
        """
        Inicializa el problema CSP para el sorteo del Mundial.
        :param teams: Diccionario con los equipos, sus confederaciones y bombos.
        :param groups: Lista con los nombres de los grupos (A-L).
        :param debug: Booleano para activar trazas de depuración.
        """
        self.teams = teams
        self.groups = groups
        self.debug = debug

        # Las variables son los equipos.
        self.variables = list(teams.keys())

        # El dominio de cada variable inicialmente son todos los grupos.
        self.domains = {team: list(groups) for team in self.variables}

    def get_team_confederation(self, team):
        return self.teams[team]["conf"]

    def get_team_pot(self, team):
        return self.teams[team]["pot"]

    def is_valid_assignment(self, group, team, assignment):
        """
        Verifica si asignar un equipo a un grupo viola
        las restricciones de confederación o tamaño del grupo.
        """
        team_conf = self.get_team_confederation(team)
        team_pot = self.get_team_pot(team)

        teams_in_group = [
            assigned_team
            for assigned_team, assigned_group in assignment.items()
            if assigned_group == group
        ]

        # Restricción de tamaño del grupo (máximo 4 equipos)
        if len(teams_in_group) >= 4:
            return False

        # Restricción de bombos y confederaciones
        uefa_count = 0
        for assigned_team in teams_in_group:
            assigned_conf = self.get_team_confederation(assigned_team)
            assigned_pot = self.get_team_pot(assigned_team)

            # No puede haber dos equipos del mismo bombo en el mismo grupo
            if assigned_pot == team_pot:
                return False

            # Restricción de confederación
            if assigned_conf == team_conf:
                if team_conf == "UEFA":
                    uefa_count += 1
                    if uefa_count >= 2:
                        return False
                else:
                    return False

        return True

    def forward_check(self, assignment, domains):
        """
        Propagación de restricciones.
        Debe eliminar valores inconsistentes en dominios futuros.
        Retorna True si la propagación es exitosa, False si algún dominio queda vacío.
        """
        # Hacemos una copia de los dominios actuales para modificarla de forma segura
        new_domains = copy.deepcopy(domains)

        # Las variables ya asignadas quedan con dominio fijo
        for team, group in assignment.items():
            new_domains[team] = [group]

        # Filtrar grupos inválidos para las variables no asignadas
        for team in self.variables:
            if team in assignment:
                continue

            valid_groups = []
            for group in new_domains[team]:
                if self.is_valid_assignment(group, team, assignment):
                    valid_groups.append(group)

            new_domains[team] = valid_groups

            if len(valid_groups) == 0:
                return False, new_domains

        return True, new_domains

    def select_unassigned_variable(self, assignment, domains):
        """
        Heurística MRV (Minimum Remaining Values).
        Selecciona la variable no asignada con el dominio más pequeño.
        """
        unassigned_vars = [var for var in self.variables if var not in assignment]

        if not unassigned_vars:
            return None

        return min(unassigned_vars, key=lambda var: len(domains[var]))

    def backtrack(self, assignment, domains=None):
        """
        Backtracking search para resolver el CSP.
        """
        if domains is None:
            domains = copy.deepcopy(self.domains)

        # Condición de parada: Si todas las variables están asignadas, retornamos la asignación.
        if len(assignment) == len(self.variables):
            return assignment

        # 1. Seleccionar variable con MRV
        team = self.select_unassigned_variable(assignment, domains)
        if team is None:
            return assignment

        # 2. Iterar sobre sus valores posibles en el dominio
        for group in domains[team]:
            if self.debug:
                print(f"Intentando asignar {team} -> Grupo {group}")

            # 3. Verificar si es válido, hacer la asignación y aplicar forward checking
            if self.is_valid_assignment(group, team, assignment):
                new_assignment = assignment.copy()
                new_assignment[team] = group

                success, new_domains = self.forward_check(new_assignment, domains)

                if success:
                    # 4. Llamada recursiva
                    result = self.backtrack(new_assignment, new_domains)
                    if result is not None:
                        return result

            if self.debug:
                print(f"Backtrack en {team} -> Grupo {group}")

        # 5. Si ningún valor funcionó, retornamos None
        return None