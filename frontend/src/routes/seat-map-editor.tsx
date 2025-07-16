import React from 'react'
import { createFileRoute } from '@tanstack/react-router'
import { LayoutCanvas } from '../components/LayoutCanvas'


export const Route = createFileRoute('/seat-map-editor')({
    component: SeatMapEditor,
})

function SeatMapEditor() {
    return(
        <div>
            <LayoutCanvas />
        </div>
    )
}