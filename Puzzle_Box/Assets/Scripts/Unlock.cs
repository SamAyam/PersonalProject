using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Unlock : MonoBehaviour {

    public GameObject keyIcon;
    public GameObject keyhole;
    public openBox openScript;
    public GameObject thisButton;
    //public string tags;

    //private void Start()
    //{
    //    GameObject h = GameObject.FindGameObjectWithTag(tags);
    //    openScript = h.GetComponent<openBox>();
    //}

    public void Turn()
    {
        if (keyIcon.activeInHierarchy)
        {
            keyhole.transform.Rotate(0, 0, 90);
            openScript.Unlock();
            thisButton.SetActive(false);
        }
    }
}
