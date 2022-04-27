# Set Origin [ft_lab.Tools.SetOrigin]

Changes the center position of the rotation or scale for the selected Mesh or Xform.    

## Usage

1. Activate "ft_lab.Tools.SetOrigin" in the Extension window.
2. Select Mesh or Xform.
3. Select "Tools"-"Set Origin"-"Center of Geometry" from the menu to move the center of the manipulator to the center of the geometry.
4. Select "Tools"-"Set Origin"-"Lower center of Geometry" from the menu to move the center of the manipulator to the lower center of the geometry.

## Operation Description

This Set Origin function adjusts the Translate and Pivot of the Prim.     

Add "ToolReplaceCenter" to omni.kit.commands.      
The argument "prim" specifies Usd.Prim.     
The argument "center_position" specifies the center position in world coordinates.     
