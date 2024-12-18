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

    # Default colors
    default_region_color = "lightblue"
    default_object_color = "gray"
    default_npc_color = "red"
    default_enemy_color = "black"

    # Iterate over regions
    for region in model.regions:
        # Use region color if specified, otherwise default
        region_color = region.color if hasattr(region, 'color') and region.color else default_region_color

        # Draw the region rectangle
        region_rect = patches.Rectangle(
            (region.position.x, region.position.y),
            region.size.width,
            region.size.height,
            linewidth=1,
            edgecolor='blue',
            facecolor=region_color,
            alpha=0.5
        )
        ax.add_patch(region_rect)

        # Display region name
        ax.text(
            region.position.x + region.size.width / 2,
            region.position.y + region.size.height + model.size.height / 100,
            region.name,
            color='blue',
            ha='center',
            va='center',
            fontsize=10
        )

        # Print region description
        print(f"Region '{region.name}': {region.description}")

        # Draw objects
        for obj in region.objects:
            obj_color = obj.color if hasattr(obj, 'color') and obj.color else default_object_color
            ax.scatter(
                region.position.x + obj.position.x,
                region.position.y + obj.position.y,
                color=obj_color,
                label=f"Object ({obj.type})" if f"Object ({obj.type})" not in ax.get_legend_handles_labels()[1] else ""
            )
            ax.text(
                region.position.x + obj.position.x,
                region.position.y + obj.position.y + model.size.height / 100,
                obj.name,
                fontsize=8,
                color=obj_color,
                ha='center'
            )

            # Print object description
            print(f"  Object '{obj.name}' ({obj.type}): {obj.description}")

        # Draw NPCs
        for npc in region.npcs:
            npc_color = npc.color if hasattr(npc, 'color') and npc.color else default_npc_color
            ax.scatter(
                region.position.x + npc.position.x,
                region.position.y + npc.position.y,
                color=npc_color,
                marker='o',
                label=f"NPC ({npc.role})" if f"NPC ({npc.role})" not in ax.get_legend_handles_labels()[1] else ""
            )
            ax.text(
                region.position.x + npc.position.x,
                region.position.y + npc.position.y + model.size.height / 100,
                npc.name,
                fontsize=8,
                color=npc_color,
                ha='center'
            )

            # Print NPC description
            print(f"  NPC '{npc.name}' ({npc.role}): {npc.description}")

        # Draw enemies
        for enemy in region.enemies:
            enemy_color = enemy.color if hasattr(enemy, 'color') and enemy.color else default_enemy_color
            ax.scatter(
                region.position.x + enemy.position.x,
                region.position.y + enemy.position.y,
                color=enemy_color,
                marker='x',
                label="Enemy" if "Enemy" not in ax.get_legend_handles_labels()[1] else ""
            )
            ax.text(
                region.position.x + enemy.position.x,
                region.position.y + enemy.position.y + model.size.height / 100,
                f"{enemy.name} ({enemy.number})",
                fontsize=8,
                color=enemy_color,
                ha='center'
            )

            # Print enemy description
            print(f"  Enemy '{enemy.name}' (x{enemy.number}): {enemy.description}")

    # Iterate over paths
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

        # Draw path
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

        # Print path description
        print(f"Path '{path.name}' from '{path.from_region.name}' to '{path.to_region.name}': {path.description}")

    ax.legend(loc="upper right")
    plt.grid(visible=True, which='both', color='gray', linestyle='--', linewidth=0.5)
    plt.show()

def main(debug=False):
    # Safely determine the directory of the script
    try:
        this_folder = dirname(__file__)
    except NameError:
        this_folder = "."

    # Load the metamodel from the grammar file
    map_mm = metamodel_from_file(join(this_folder, 'RPGMAPR.tx'), debug=debug)

    # Export the metamodel if debugging is enabled
    if debug:
        metamodel_export(map_mm, join(this_folder, 'RPGMAPR_meta.dot'))

    # Ask user to input the map to be modeled
    filename = input("Map to be displayed: ")

    # Load the map model 
    map_model = map_mm.model_from_file(join(this_folder, filename))

    # Export the model if debugging is enabled
    if debug:
        model_export(map_model, join(this_folder, 'test_model.dot'))

    # Draw the map using the parsed model
    draw_map(map_model)

if __name__ == "__main__":
    main(debug=True)
