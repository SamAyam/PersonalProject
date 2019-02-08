using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class QuitButtonScript : MonoBehaviour {


	
	public void QuitApp ()
    {
        if (AppControl.control.autosave)
        {
            AppControl.control.Save();
        }
        Application.Quit();
	}
}
