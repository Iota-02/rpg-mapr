from os.path import dirname, join
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_map(model):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, model.size.width)
    ax.set_ylim(0, model.size.height)
    ax.set_title(f"Map: {model.name}", fontsize=16)
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")

    object_colors = {
        "landmark": "green",
        "object": "darkred",
        "structure": "gold",
    }
    npc_markers = {
        "quest giver": "o",
        "information": "D",
        "shopkeeper": "s",
    }
    enemy_marker = "x"

    for region in model.regions:
        region_rect = patches.Rectangle(
            (region.position.x, region.position.y),
            region.size.width,
            region.size.height,
            linewidth=1,
            edgecolor='blue',
            facecolor='lightblue',
            alpha=0.5
        )
        ax.add_patch(region_rect)
        ax.text(
            region.position.x + region.size.width / 2,
            region.position.y + region.size.height + model.size.height/100,
            region.name,
            color='blue',
            ha='center',
            va='center',
            fontsize=10
        )

        for obj in region.objects:
            color = object_colors.get(obj.type, "gray")
            ax.scatter(
                region.position.x + obj.position.x,
                region.position.y + obj.position.y,
                color=color,
                label=f"Object ({obj.type})" if f"Object ({obj.type})" not in ax.get_legend_handles_labels()[1] else ""
            )
            ax.text(
                region.position.x + obj.position.x,
                region.position.y + obj.position.y + 1,
                obj.name,
                fontsize=8,
                color=color,
                ha='center'
            )

        for npc in region.npcs:
            marker = npc_markers.get(npc.role, "o")
            ax.scatter(
                region.position.x + npc.position.x,
                region.position.y + npc.position.y,
                color="red",
                marker=marker,
                label=f"NPC ({npc.role})" if f"NPC ({npc.role})" not in ax.get_legend_handles_labels()[1] else ""
            )
            ax.text(
                region.position.x + npc.position.x,
                region.position.y + npc.position.y + 1,
                npc.name,
                fontsize=8,
                color="red",
                ha='center'
            )

        for enemy in region.enemies:
            ax.scatter(
                region.position.x + enemy.position.x,
                region.position.y + enemy.position.y,
                color="black",
                marker=enemy_marker,
                label="Enemy" if "Enemy" not in ax.get_legend_handles_labels()[1] else ""
            )
            ax.text(
                region.position.x + enemy.position.x,
                region.position.y + enemy.position.y + 1,
                f"{enemy.name} ({enemy.number})",
                fontsize=8,
                color="black",
                ha='center'
            )

    for path in model.paths:
        start_region = next(r for r in model.regions if r.name == path.from_region.name)
        end_region = next(r for r in model.regions if r.name == path.to_region.name)

        start_center = (
            start_region.position.x + start_region.size.width / 2,
            start_region.position.y + start_region.size.height / 2
        )
        end_center = (
            end_region.position.x + end_region.size.width / 2,
            end_region.position.y + end_region.size.height / 2
        )

        ax.plot(
            [start_center[0], end_center[0]],
            [start_center[1], end_center[1]],
            color='brown',
            linestyle='dotted',
            label="Path" if 'Path' not in ax.get_legend_handles_labels()[1] else ""
        )
        ax.text(
            (start_center[0] + end_center[0]) / 2,
            (start_center[1] + end_center[1]) / 2,
            path.name,
            fontsize=8,
            color='brown',
            ha='center'
        )

    ax.legend(loc="upper right")
    plt.grid(visible=True, which='both', color='gray', linestyle='--', linewidth=0.5)
    plt.show()

def main(debug=False):
    # Safely determine the directory of the script
    try:
        # `__file__` works in normal script execution
        this_folder = dirname(__file__)
    except NameError:
        # Fallback for environments like Jupyter Notebook or certain IDEs
        this_folder = "."

    # Load the metamodel from the grammar file
    map_mm = metamodel_from_file(join(this_folder, 'RPGMAPR.tx'), debug=debug)

    # Export the metamodel if debugging is enabled
    if debug:
        metamodel_export(map_mm, join(this_folder, 'RPGMAPR_meta.dot'))

    # Load the map model from the test file
    map_model = map_mm.model_from_file(join(this_folder, 'test.map'))

    # Export the model if debugging is enabled
    if debug:
        model_export(map_model, join(this_folder, 'test_model.dot'))

    # Draw the map using the parsed model
    draw_map(map_model)


if __name__ == "__main__":
    main(debug=True)