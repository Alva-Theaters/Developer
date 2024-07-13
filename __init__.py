# This file is part of Alva Sorcerer.
# Copyright (C) 2024 Alva Theaters

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


'''
=====================================================================
                      DESIGNED BY ALVA THEATERS
                       FOR THE SOLE PURPOSE OF
                         MAKING PEOPLE HAPPY
=====================================================================
'''


## Double hashtag indicates notes for future development requiring some level of attention


import bpy


bl_info = {
    "author": "Alva Theaters",
    "name": "Alva Developer",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "category": "Text Editor",
    "description": "Makes it easier to manage many text blocks."
}


def update_current_text(self, context):
    index = context.scene.alva_sorcerer_text_block_index
    text_blocks = context.scene.alva_sorcerer_text_blocks
    
    if 0 <= index < len(text_blocks):
        text_name = text_blocks[index].name
        bpy.context.area.spaces.active.text = bpy.data.texts.get(text_name)


class TextBlockItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name")
    include: bpy.props.BoolProperty(name="Include", default=False)


class TEXT_UL_TextBlockList(bpy.types.UIList):
    """UIList for displaying text blocks."""
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        text_block = item
        layout.label(text=text_block.name)
        layout.prop(text_block, "include", text="", toggle=False)


class TEXT_OT_RunSelectedScripts(bpy.types.Operator):
    """Run selected scripts"""
    bl_idname = "text.run_selected_scripts"
    bl_label = "Run selected scripts"
    
    def execute(self, context):
        text_data = context.scene.alva_sorcerer_text_blocks
        for text_block in text_data:
            if text_block.include:
                script = bpy.data.texts.get(text_block.name)
                if script:
                    exec(script.as_string(), {'__name__': '__main__', '__file__': ''})
        return {'FINISHED'}


class TEXT_OT_UpdateTextBlocks(bpy.types.Operator):
    """Update text blocks list"""
    bl_idname = "text.update_text_blocks"
    bl_label = "Update text blocks"
    
    def execute(self, context):
        text_data = context.scene.alva_sorcerer_text_blocks
        
        existing_names = {item.name: item for item in text_data}
        current_names = {text.name for text in bpy.data.texts}
        
        # Remove items that are no longer in bpy.data.texts
        for name in list(existing_names.keys()):
            if name not in current_names:
                index = next(i for i, item in enumerate(text_data) if item.name == name)
                text_data.remove(index)
        
        # Add new items that are in bpy.data.texts but not in text_data
        for name in current_names:
            if name not in existing_names:
                item = text_data.add()
                item.name = name
        
        return {'FINISHED'}


class TEXT_OT_MoveTextBlockUp(bpy.types.Operator):
    """Move text block up"""
    bl_idname = "text.move_text_block_up"
    bl_label = "Move Up"
    
    def execute(self, context):
        index = context.scene.alva_sorcerer_text_block_index
        text_blocks = context.scene.alva_sorcerer_text_blocks
        
        if index > 0:
            text_blocks.move(index, index - 1)
            context.scene.alva_sorcerer_text_block_index -= 1
        
        return {'FINISHED'}


class TEXT_OT_MoveTextBlockDown(bpy.types.Operator):
    """Move text block down"""
    bl_idname = "text.move_text_block_down"
    bl_label = "Move Down"
    
    def execute(self, context):
        index = context.scene.alva_sorcerer_text_block_index
        text_blocks = context.scene.alva_sorcerer_text_blocks
        
        if index < len(text_blocks) - 1:
            text_blocks.move(index, index + 1)
            context.scene.alva_sorcerer_text_block_index += 1
        
        return {'FINISHED'}


class TEXT_PT_AlvaDeveloperPanel(bpy.types.Panel):
    """Creates a Panel in the Text Editor"""
    bl_label = "Alva Developer"
    bl_idname = "TEXT_PT_AlvaDeveloper"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Alva Developer'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        active_text = bpy.context.area.spaces.active.text
        
        row = layout.row(align=True)
        row.prop(active_text, "name", text="")
        row.operator("text.move_text_block_up", text="", icon='TRIA_UP')
        row.operator("text.move_text_block_down", text="", icon='TRIA_DOWN')
        
        row = layout.row()
        row.template_list("TEXT_UL_TextBlockList", "", scene, "alva_sorcerer_text_blocks", scene, "alva_sorcerer_text_block_index")

        row = layout.row()
        row.operator("text.update_text_blocks", text="Update Text Blocks", icon='FILE_REFRESH')
        row = layout.row()
        row.operator("text.run_selected_scripts", text="Run Selected Scripts", icon='PLAY')


classes = [
    TextBlockItem,
    TEXT_UL_TextBlockList,
    TEXT_OT_RunSelectedScripts,
    TEXT_OT_UpdateTextBlocks,
    TEXT_OT_MoveTextBlockUp,
    TEXT_OT_MoveTextBlockDown,
    TEXT_PT_AlvaDeveloperPanel,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.alva_sorcerer_text_blocks = bpy.props.CollectionProperty(type=TextBlockItem)
    bpy.types.Scene.alva_sorcerer_text_block_index = bpy.props.IntProperty(name="Index", default=0, update=update_current_text)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.alva_sorcerer_text_blocks
    del bpy.types.Scene.alva_sorcerer_text_block_index
