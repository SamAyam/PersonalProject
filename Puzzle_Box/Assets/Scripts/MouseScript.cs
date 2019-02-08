using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MouseScript : MonoBehaviour {
    public bool holding;
    private Vector3 mousePosition;

    // Use this for initialization
    void Start()
    {
        holding = false;
    }

    public void Hold()
    {
        holding = true;
    }

    public void Drop()
    {
        holding = false;
    }

    // Update is called once per frame
    void Update()
    {

        mousePosition = Input.mousePosition;
        mousePosition = Camera.main.ScreenToWorldPoint(mousePosition);
        transform.position = mousePosition;

    }
}
