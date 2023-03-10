import gurobipy as gp


def merge_mg_lps(lp_files: list, output_file: str, verbose: bool = False):
    """
    merge multiple LPs into one
    """

    # Step 1: we read the first LP
    model = gp.read(lp_files[0])

    # Step 2: we add the other LPs
    for i in range(1, len(lp_files)):
        new_model = gp.read(lp_files[i])

        # there are some linear programs that we need to skip
        # because they are not related to the problem

        is_related_to_throughput = False
        for var in new_model.getVars():
            if "_slots" in var.varName:
                is_related_to_throughput = True
                break

            if "_flop" in var.varName:
                is_related_to_throughput = True
                break

            if "_hasBuffer" in var.VarName:
                is_related_to_throughput = True
                break

        if not is_related_to_throughput:
            continue

        for var in new_model.getVars():

            model.addVar(vtype=var.vtype, name=var.VarName, lb=var.lb, ub=var.ub)

            if verbose:
                print(f"add variable {var.varName}")

        model.update()

        for constr in new_model.getConstrs():

            row: gp.LinExpr = new_model.getRow(constr)

            coeffs = []
            var_names = []

            for i in range(row.size()):
                coeffs.append(row.getCoeff(i))
                var_names.append(row.getVar(i).VarName)

            vars = [model.getVarByName(var_name) for var_name in var_names]

            lhs = gp.LinExpr(coeffs, vars)

            model.addConstr(lhs, constr.Sense, constr.RHS)

            if verbose:
                print(
                    f"add constraint {new_model.getRow(constr)} {constr.Sense} {constr.RHS}"
                )

        model.update()

        objective = model.getObjective()
        new_objective = new_model.getObjective()

        coeffs = []
        var_names = []

        for i in range(new_objective.size()):
            coeffs.append(new_objective.getCoeff(i))
            var_names.append(new_objective.getVar(i).VarName)

        vars = [model.getVarByName(var_name) for var_name in var_names]

        for i in range(new_objective.size()):
            # we need to all check the sense of the objective
            # if the sense is minimization, we need to add the coefficients

            if model.ModelSense == new_model.ModelSense:
                objective.add(vars[i], coeffs[i])
            else:
                objective.add(vars[i], -coeffs[i])

        model.setObjective(objective, sense=model.ModelSense)
        model.update()

    # Step 3: we write the merged LP
    model.write(output_file)
