using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DragItem : MonoBehaviour {
    //public bool mouse;
    public MouseScript hold;
    public GameObject item;
    //public GameObject button;
    public GameObject icon;
    private bool clicked = false;

 //   public bool clicked;

	//// Use this for initialization
	void Start () {
        GameObject h = GameObject.FindGameObjectWithTag("Hand");
        hold = h.GetComponent<MouseScript> ();
    }
	
	// Update is called once per frame
	void Update ()
    {
        if (Input.GetMouseButton(0) && hold.holding)
        {
            clicked = true;
        }
        else if (clicked == true)
        { 
            hold.holding = false;
            icon.SetActive(false);
            item.SetActive(true);
            //button.SetActive(true);
            Cursor.visible = true;
            clicked = false;
        }

    }

    public void Pickup ()
    {
        if (!hold.holding)
        {
            hold.holding = true;
            icon.SetActive(true);
            item.SetActive(false);
            //button.SetActive(false);
            Cursor.visible = false;
        }
    }
}
