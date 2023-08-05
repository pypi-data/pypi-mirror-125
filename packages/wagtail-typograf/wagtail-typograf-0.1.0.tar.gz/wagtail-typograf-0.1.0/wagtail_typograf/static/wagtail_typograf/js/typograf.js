const React = window.React;
const EditorState = window.DraftJS.EditorState;
const createEditorStateFromRaw = window.Draftail.createEditorStateFromRaw;
const serialiseEditorStateToRaw = window.Draftail.serialiseEditorStateToRaw;

// Not a real React component – just creates the entities as soon as it is rendered.
class TypografSource extends React.Component {
    async componentDidMount() {
        const apiUrl = '/api/typograf/';
        const { editorState, entityType, onComplete } = this.props;

        const rawContent = serialiseEditorStateToRaw(editorState);
        const response = await fetch(
            apiUrl, {
                body: JSON.stringify(rawContent),
                method: 'POST',
            }
        ).then(response => response.json());

        const newContent = createEditorStateFromRaw(response.data).getCurrentContent();
        const nextState = EditorState.push(editorState, newContent, 'adjust-depth')

        onComplete(nextState);
    }

    render() {
        return null;
    }
}

window.draftail.registerPlugin({
    type: 'TYPOGRAF',
    source: TypografSource,
});
