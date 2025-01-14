//Imports
import 'package:flutter/material.dart';
import 'package:client/apiInterface.dart';

/*
NOTE
################################################################################
This is the template used to create the widget that would display the history 
results in the history page.
################################################################################
*/

//Code
class HistoryItem extends StatefulWidget {
  const HistoryItem(
      {super.key, required this.equation, required this.problemID});

  final String equation, problemID;

  @override
  State<HistoryItem> createState() => _HistoryItemState();
}

class _HistoryItemState extends State<HistoryItem> {
  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.fromLTRB(50.0, 10.0, 50.0, 0),
      child: Padding(
        padding: const EdgeInsets.fromLTRB(10.0, 10.0, 10.0, 10.0),
        child: ListTile(
          //onTap: goToEquation,
          title: Text(
            widget.equation,
            style: TextStyle(
              letterSpacing: 2.0,
              wordSpacing: 4.5,
              fontSize: 24.0,
            ),
          ),
          leading: Icon(Icons.history),
          trailing: Icon(Icons.arrow_forward_ios),
        ),
      ),
    );
  }

  /* void goToEquation() {
    Navigator.push(
        context,
        MaterialPageRoute(
            builder: (context) => EquationOverview(
                equation: widget.equation,
                conf_score: widget.conf_score,
                problemID: widget.problemID)));
  } */
}
