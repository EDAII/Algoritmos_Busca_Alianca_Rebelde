# missoes_busca/busca_interpolar.py

def interpolation_search(arr, target, on_step=None, max_steps=10_000):
    """
    Busca por Interpolação (iterativa).
    Requer `arr` ordenado (idealmente ~uniforme).
    Retorna (index, steps). Se index == -1, não encontrado.

    Parâmetros:
        arr (list[int|float]): lista ordenada crescente.
        target (int|float): valor a procurar.
        on_step (callable|None): callback por iteração com o estado:
            {
              "low": low, "high": high, "pos": pos,
              "arr_low": arr[low], "arr_high": arr[high],
              "pos_val": arr[pos],
              "cmp": "lt|gt|eq|div_zero|out_of_range|empty"
            }
        max_steps (int): limite de segurança.
    """
    if not arr:
        if on_step:
            on_step({"low": -1, "high": -1, "pos": -1,
                     "arr_low": None, "arr_high": None,
                     "pos_val": None, "cmp": "empty"})
        return -1, 0

    low, high = 0, len(arr) - 1
    steps = 0

    # Saída rápida se alvo fora do intervalo
    if target < arr[low] or target > arr[high]:
        if on_step:
            on_step({"low": low, "high": high, "pos": -1,
                     "arr_low": arr[low], "arr_high": arr[high],
                     "pos_val": None, "cmp": "out_of_range"})
        return -1, steps

    while low <= high and steps < max_steps:
        steps += 1

        # Evita divisão por zero quando arr[low] == arr[high]
        if arr[high] == arr[low]:
            pos = low
            cmp_type = "div_zero"
        else:
            # Fórmula da interpolação (estimativa de posição)
            pos = low + int((target - arr[low]) * (high - low) / (arr[high] - arr[low]))
            # Clampeia para [low, high]
            pos = max(low, min(pos, high))
            cmp_type = None

        pos_val = arr[pos]

        if pos_val == target:
            if on_step:
                on_step({"low": low, "high": high, "pos": pos,
                         "arr_low": arr[low], "arr_high": arr[high],
                         "pos_val": pos_val, "cmp": "eq"})
            return pos, steps

        if cmp_type == "div_zero":
            # Lista achatada localmente; faz passo simples
            if pos_val < target:
                low = pos + 1
                out = "lt"
            else:
                high = pos - 1
                out = "gt"
            if on_step:
                on_step({"low": low, "high": high, "pos": pos,
                         "arr_low": arr[low] if low < len(arr) else None,
                         "arr_high": arr[high] if high >= 0 else None,
                         "pos_val": pos_val, "cmp": out})
            continue

        if target < pos_val:
            high = pos - 1
            if on_step:
                on_step({"low": low, "high": high, "pos": pos,
                         "arr_low": arr[low],
                         "arr_high": arr[high] if high >= 0 else None,
                         "pos_val": pos_val, "cmp": "gt"})
        else:
            low = pos + 1
            if on_step:
                on_step({"low": low, "high": high, "pos": pos,
                         "arr_low": arr[low] if low < len(arr) else None,
                         "arr_high": arr[high],
                         "pos_val": pos_val, "cmp": "lt"})

    return -1, steps
