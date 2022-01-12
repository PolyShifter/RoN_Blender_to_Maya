# RoN_Blender_to_Maya
This is a tool I have developed to use your existing version of Blender and port over the `.psk` files into Maya.

It imports the psk into Blender using a batch process and sets the scale correctly before exporting as an fbx to your designated location.
You then have the option of importing it into Maya and allowing it to automatically be cleaned by the tool, or manually importing it, OR setting the `fix_fbx` argument to `False`.


## INSTALL GUIDE

Ensure the folder `btom_psk` is located in your `documents/maya/scripts/` folder. IE:
`C:/Users/<YOUR USER NAME>/Documents/maya/scripts/btom_psk`

Create a shelf button and in the Python tab include this code:
```
from btom_psk import maya_ui_psk_to_fbx as btom

spk_to_fbx = btom.ConvertPSKToFBX(fix_fbx=True)
spk_to_fbx.show()
```

When running the tool, make sure to select your `Blender.exe` file, the `psk` or `pskx` file, and then a save location/name.
After clicking the `Convert!` button it will be greyed out and a loading bar will appear. When the bar has filled you should now have
your `Convert!` button replaced with an `Import FBX` button. Click that button and it will bring in that `.fbx` file you saved and clean up it's naming and hierarchy.

NOTE!! Your root bone for your skeleton, should be either `J_Gun` (for weapon meshes) or `root` (for body meshes) or something like that. I have encountered some files like the `Fiveseven` that actually has an additional root bone before `J_Gun`. But simply unparenting `J_Gun` to the world and deleting the other bone, we then have a working skeleton for RorN.

Happy modding and I hope this works well for you!
If you have any questions or need a fix for this hit me up here or on discord:
PolyShifter#4816
