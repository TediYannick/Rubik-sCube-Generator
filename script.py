import bpy

class RubiksCubePanel(bpy.types.Panel):
    bl_label = "Rubik's Cube Generator"
    bl_idname = "OBJECT_PT_rubikscube"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.prop(scene, "cube_size")
        row = layout.row()
        row.prop(scene, "padding")
        row = layout.row()
        row.prop(scene, "bevel_width")
        row = layout.row()
        row.prop(scene, "cube_dimension")
        row = layout.row()
        row.operator("object.generate_rubikscube")

class GenerateRubiksCubeOperator(bpy.types.Operator):
    bl_idname = "object.generate_rubikscube"
    bl_label = "Generate Rubik's Cube"

    def execute(self, context):
        
        # Supprimer tous les objets de la scène
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        # Accéder aux propriétés de la scène
        cube_size = context.scene.cube_size
        padding = context.scene.padding
        bevel_width = context.scene.bevel_width
        dimension = context.scene.cube_dimension

        # Taille totale d'un cube avec l'espacement
        total_size = cube_size + padding

        # Couleurs pour chaque face du Rubik's Cube
        colors = ['RED', 'GREEN', 'BLUE', 'YELLOW', 'WHITE', 'ORANGE']

        # Créer un matériau pour chaque couleur
        materials = {}
        for color in colors:
            mat = bpy.data.materials.new(name=color)
            if color == 'RED':
                mat.diffuse_color = (1, 0, 0, 1)
            elif color == 'GREEN':
                mat.diffuse_color = (0, 1, 0, 1)
            elif color == 'BLUE':
                mat.diffuse_color = (0, 0, 1, 1)
            elif color == 'YELLOW':
                mat.diffuse_color = (1, 1, 0, 1)
            elif color == 'WHITE':
                mat.diffuse_color = (1, 1, 1, 1)
            elif color == 'ORANGE':
                mat.diffuse_color = (1, 0.5, 0, 1)
            materials[color] = mat

        # Créer un matériau noir pour les biseaux
        bevel_mat = bpy.data.materials.new(name='BLACK')
        bevel_mat.diffuse_color = (0, 0, 0, 1)

        # Créer un cube à chaque position dans une grille NxNxN
        offset = (dimension - 1) / 2
        for x in range(dimension):
            for y in range(dimension):
                for z in range(dimension):
                    # Calculer la position du cube
                    position = ((x - offset) * total_size, (y - offset) * total_size, (z - offset) * total_size)

                    # Créer le cube
                    bpy.ops.mesh.primitive_cube_add(size=cube_size, location=position)

                    # Ajouter les matériaux au cube
                    cube = bpy.context.object
                    for i, color in enumerate(colors):
                        cube.data.materials.append(materials[color])
                        for face in cube.data.polygons:
                            if face.normal[i % 3] == 1.0 and face.center[i % 3] > 0:
                                face.material_index = i
                            elif face.normal[i % 3] == -1.0 and face.center[i % 3] < 0:
                                face.material_index = (i + 3) % 6

                    # Ajouter un bevel au cube
                    bpy.ops.object.modifier_add(type='BEVEL')
                    bpy.context.object.modifiers["Bevel"].width = bevel_width
                    bpy.context.object.modifiers["Bevel"].material = len(cube.data.materials)

                    # Ajouter le matériau noir au cube
                    cube.data.materials.append(bevel_mat)

                    # Applique shadesmooth au cube
                    bpy.ops.object.shade_smooth()
                    
        return {'FINISHED'}

def register():
    bpy.utils.register_class(RubiksCubePanel)
    bpy.utils.register_class(GenerateRubiksCubeOperator)
    bpy.types.Scene.cube_size = bpy.props.FloatProperty(name="Cube Size", default=1.0)
    bpy.types.Scene.padding = bpy.props.FloatProperty(name="Padding", default=0.01)
    bpy.types.Scene.bevel_width = bpy.props.FloatProperty(name="Bevel Width", default=0.1)
    bpy.types.Scene.cube_dimension = bpy.props.IntProperty(name="Cube Dimension", default=3, min=2, max=10)

def unregister():
    bpy.utils.unregister_class(RubiksCubePanel)
    bpy.utils.unregister_class(GenerateRubiksCubeOperator)
    del bpy.types.Scene.cube_size
    del bpy.types.Scene.padding
    del bpy.types.Scene.bevel_width
    del bpy.types.Scene.cube_dimension

if __name__ == "__main__":
    register()
